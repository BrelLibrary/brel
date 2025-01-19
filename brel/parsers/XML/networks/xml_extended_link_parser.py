"""
This module parses XML extended links into one or multiple networks.
Networks are covered in the XBRL Generic Links spec.
https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html

====================

- author: Robin Schmidiger
- version: 0.14
- date: 29 January 2024

====================
"""

import itertools
import time
from collections import defaultdict
from typing import Any, cast, Mapping, Iterable

import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import *
from brel.parsers.XML.networks import (
    CalculationNetworkFactory,
    FootnoteNetworkFactory,
    IXMLNetworkFactory,
    LabelNetworkFactory,
    LogicalDefinitionNetworkFactory,
    PhysicalDefinitionNetworkFactory,
    PresentationNetworkFactory,
    ReferenceNetworkFactory,
    parse_xml_resource,
)
from brel.parsers.utils import get_str
from brel.reportelements import *
from brel.resource import *

DEBUG = False


def get_object_from_reference(
    referenced_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    id_to_any: Mapping[str, Any],
) -> IResource | IReportElement | Fact:
    """
    Given a locator or resource element, get the object that the reference points to.
    :param referenced_element: The locator or resource element.
    :param qname_nsmap: The QNameNSMap of the filing.
    :param id_to_any: A dict mapping xml ids to report elements and resources.
    :returns IResource|IReportElement|Fact: The object that the reference points to.
    :raises ValueError: If the referenced element does not have a xlink:type attribute with value 'locator' or 'resource'.
    """

    nsmap = qname_nsmap.get_nsmap()
    referenced_element_type = referenced_element.get(f"{{{nsmap['xlink']}}}type", "")

    if referenced_element_type == "locator":
        # if the referenced element is a locator, get the referenced element from the report elements
        if referenced_element.get(f"{{{nsmap['xlink']}}}type", "") != "locator":
            raise ValueError(
                f"the locator_xml element {referenced_element.tag} does not have a xlink:type attribute with value 'locator'"
            )

        to_element: IReportElement | IResource | Fact | None = None

        # get the href attribute
        href = cast(str, referenced_element.get(f"{{{nsmap['xlink']}}}href", ""))

        if "#" in href:
            _, elem_id = href.split("#")
        else:
            elem_id = href

        if elem_id not in id_to_any:
            raise ValueError(f"the referenced element {elem_id} could not be found")
        to_element = id_to_any.get(elem_id)

    elif referenced_element_type == "resource":
        to_element = parse_xml_resource(referenced_element, qname_nsmap.get_nsmap())
    else:
        raise NotImplementedError(f"the referenced element type {referenced_element_type} is not supported")

    if to_element is None:
        raise ValueError(f"the referenced element {referenced_element} could not be found")

    return to_element


def parse_xml_link(
    xml_link_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    id_to_any: Mapping[str, Any],
    report_elements: Mapping[QName, IReportElement],
) -> Iterable[INetwork]:
    """
    Parse an xml link element into one or multiple networks.
    :param xml_link_element: The xml link element to parse.
    :param qname_nsmap: The QNameNSMap of the filing.
    :param id_to_any: A dict mapping xml ids to report elements and resources.
    :param report_elements: A dict mapping QNames to report elements.
    :returns list[INetwork]: A list of networks
    :raises NotImplementedError: If the link element is not supported.
    :raises ValueError: If the link is malformed.
    """
    nsmap = qname_nsmap.get_nsmap()

    networks: list[INetwork] = []

    # Create the right network factories depending on the link element
    # instead of being a single factory, this is a list.
    # Why? Because for some networks (i.e. definition networks), we want to do multiple passes over the linkbase with different factories
    network_factories: list[IXMLNetworkFactory] = []

    if xml_link_element.tag == f"{{{nsmap['link']}}}presentationLink":
        network_factories.append(PresentationNetworkFactory(qname_nsmap))
    elif xml_link_element.tag == f"{{{nsmap['link']}}}calculationLink":
        network_factories.append(CalculationNetworkFactory(qname_nsmap))
    elif xml_link_element.tag == f"{{{nsmap['link']}}}definitionLink":
        # for definition networks we need to create both a physical and a logical network
        network_factories.append(PhysicalDefinitionNetworkFactory(qname_nsmap))
        network_factories.append(LogicalDefinitionNetworkFactory(qname_nsmap))
    elif xml_link_element.tag == f"{{{nsmap['link']}}}labelLink":
        network_factories.append(LabelNetworkFactory(qname_nsmap))
    elif xml_link_element.tag == f"{{{nsmap['link']}}}referenceLink":
        network_factories.append(ReferenceNetworkFactory(qname_nsmap))
    elif xml_link_element.tag == f"{{{nsmap['link']}}}footnoteLink":
        network_factories.append(FootnoteNetworkFactory(qname_nsmap))
    else:
        raise NotImplementedError(f"the link element {xml_link_element.tag} is not supported")

    for network_factory in network_factories:
        nodes_lookup: dict[str, list[INetworkNode]] = defaultdict(list)
        edges: set[tuple[str, str, str]] = set()
        node_to_arcs: dict[str, list[lxml.etree._Element]] = defaultdict(list)
        roots: set[INetworkNode] = set()

        # first pass. Iterate over all elements in the linkbase, create the nodes and edges
        if DEBUG:  # pragma: no cover
            start_time = time.time()

        for arc_element in xml_link_element.findall(f".//*[@xlink:type='arc']", namespaces=nsmap):
            arc_from = get_str(arc_element, f"{{{nsmap['xlink']}}}from")
            arc_to = get_str(arc_element, f"{{{nsmap['xlink']}}}to")
            arc_role = get_str(arc_element, f"{{{nsmap['xlink']}}}arcrole")

            if (arc_from, arc_to, arc_role) in edges:
                # the edge already exists. The SEC XBRL Filing Manual says that this is an error.
                raise ValueError(f"the arc element with from='{arc_from}' and to='{arc_to}' is a duplicate")

            edges.add((arc_from, arc_to, arc_role))
            node_to_arcs[arc_from].append(arc_element)
            node_to_arcs[arc_to].append(arc_element)

        # iterate over all locators or resources
        for link_element in xml_link_element.xpath(  # type: ignore
            f".//*[@xlink:type='resource' or @xlink:type='locator']", namespaces=nsmap  # type: ignore
        ):  # type: ignore
            if not isinstance(link_element, lxml.etree._Element):
                raise TypeError(
                    f"the xpath query did not return a list of lxml.etree._Element. Instead, it returned {type(link_element)}"
                )

            label = get_str(link_element, f"{{{nsmap['xlink']}}}label")
            to_object = get_object_from_reference(link_element, qname_nsmap, id_to_any)
            node_arcs = node_to_arcs[label]
            # try finding an arc where 'to' points to the current resource/locator
            arcs_to = list(
                filter(
                    lambda arc: arc.get(f"{{{nsmap['xlink']}}}to", "") == label,
                    node_arcs,
                )
            )
            arcs_from = list(
                filter(
                    lambda arc: arc.get(f"{{{nsmap['xlink']}}}from", "") == label,
                    node_arcs,
                )
            )

            if network_factory.is_physical():
                if len(arcs_to) == 0 and len(arcs_from) == 0:
                    # the node is not connected to any other node. The network only contains this node
                    node = network_factory.create_node(xml_link_element, link_element, None, to_object)
                    roots.add(node)
                    nodes_lookup[label].append(node)
                else:
                    outgoing_role_types = set(get_str(arc, f"{{{nsmap['xlink']}}}arcrole") for arc in arcs_from)

                    incoming_role_types = set(get_str(arc, f"{{{nsmap['xlink']}}}arcrole") for arc in arcs_to)

                    for role_type in incoming_role_types.union(outgoing_role_types):
                        # sort node_arcs such that the arcs with xlink:to == label come first
                        node_arcs.sort(
                            key=lambda arc: arc.get(f"{{{nsmap['xlink']}}}to") == label,
                            reverse=True,
                        )

                        arc = next(
                            (arc for arc in node_arcs if get_str(arc, f"{{{nsmap['xlink']}}}arcrole") == role_type),
                            None,
                        )

                        node = network_factory.create_node(xml_link_element, link_element, arc, to_object)

                        if role_type not in incoming_role_types:
                            roots.add(node)
                        nodes_lookup[label].append(node)

            else:
                if len(arcs_to) == 0 and len(arcs_from) == 0:
                    # the node is not connected to any other node. The network only contains this node
                    node = network_factory.create_node(xml_link_element, link_element, None, to_object)
                    roots.add(node)
                    nodes_lookup[label].append(node)
                else:
                    arc = arcs_to[0] if len(arcs_to) > 0 else arcs_from[0]

                    node = network_factory.create_node(xml_link_element, link_element, arc, to_object)

                    if len(arcs_to) == 0:
                        roots.add(node)
                    nodes_lookup[label].append(node)

        if DEBUG:  # pragma: no cover
            end_time = time.time()
            print(f"first pass took {end_time - start_time:.2f} seconds")
            start_time = time.time()

        # second pass. Create the tree by iterating over the edges and adding the edge's 'to' node as a child to the edge's 'from' node
        for arc_from, arc_to, arc_role in edges:
            from_nodes = nodes_lookup[arc_from]
            to_nodes = nodes_lookup[arc_to]

            if network_factory.is_physical():
                from_nodes = list(filter(lambda node: node.get_arc_role() == arc_role, from_nodes))
                to_nodes = list(filter(lambda node: node.get_arc_role() == arc_role, to_nodes))

            for from_node, to_node in itertools.product(from_nodes, to_nodes):
                # Now we can link the nodes
                from_node._add_child(to_node)

        # third pass. If the network is physical, create a network for each arcrole in the roots
        # if the network is logical (not physical), create a single network with all the roots
        # Networks have to be non-empty, so if there are no roots, we skip this step
        if len(roots) == 0:
            continue

        if DEBUG:  # pragma: no cover
            end_time = time.time()
            print(f"second pass took {end_time - start_time:.2f} seconds")
            start_time = time.time()

        if network_factory.is_physical():
            # get all role types in the roots
            role_types = set(node.get_arc_role() for node in roots)
            # create a network for each role type. the roots of this network are the nodes with the same role type
            for role_type in role_types:
                role_type_roots = [node for node in roots if node.get_arc_role() == role_type]
                network = network_factory.create_network(xml_link_element, role_type_roots)
                # update the report elements
                report_elements = network_factory.update_report_elements(report_elements, network)
                # add the network to the networks list
                networks.append(network)
        else:
            # create a network with all the roots
            root_nodes = list(roots)
            network = network_factory.create_network(xml_link_element, root_nodes)
            # update the report elements
            report_elements = network_factory.update_report_elements(report_elements, network)
            # add the network to the networks list
            networks.append(network)

    if DEBUG:  # pragma: no cover
        end_time = time.time()
        print(f"third pass took {end_time - start_time:.2f} seconds")

    return networks
