"""
This module parses XML extended links into one or multiple networks.
Networks are covered in the XBRL Generic Links spec.
https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html

====================

- author: Robin Schmidiger
- version: 0.16
- date: 9 May 2025

====================
"""

import itertools
from collections import defaultdict
from typing import Iterable

import lxml.etree

from brel.brel_fact import Fact
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
from brel.parsers.utils.lxml_utils import find_elements, get_str_attribute, get_str_tag
from brel.reportelements import *
from brel.resource import *
from brel.contexts.filing_context import FilingContext


def get_object_from_reference(
    referenced_element: lxml.etree._Element,  # type: ignore
    filing_context: FilingContext,
) -> IResource | IReportElement | Fact:
    report_element_repository = filing_context.get_report_element_repository()
    fact_repository = filing_context.get_fact_repository()

    referenced_element_type = get_str_attribute(referenced_element, "xlink:type")

    if referenced_element_type == "locator":
        locator_target_element: IReportElement | IResource | Fact | None = None

        href = get_str_attribute(referenced_element, "xlink:href")

        elem_id = href.split("#")[-1]

        if report_element_repository.has_id(elem_id):
            locator_target_element = report_element_repository.get_by_id(elem_id)
        elif fact_repository.has_id(elem_id):
            locator_target_element = fact_repository.get_by_id(elem_id)
        else:
            raise ValueError(f"the referenced element {elem_id} could not be found")

    elif referenced_element_type == "resource":
        locator_target_element = parse_xml_resource(referenced_element)
    else:
        raise NotImplementedError(
            f"the referenced element type {referenced_element_type} is not supported"
        )

    return locator_target_element


def parse_xml_link(
    context: FilingContext,
    xml_link_element: lxml.etree._Element,  # type: ignore
) -> Iterable[INetwork]:
    networks: list[INetwork] = []
    network_factories: list[IXMLNetworkFactory] = []

    if "presentationLink" in get_str_tag(xml_link_element):
        network_factories.append(PresentationNetworkFactory())
    elif "calculationLink" in get_str_tag(xml_link_element):
        network_factories.append(CalculationNetworkFactory())
    elif "definitionLink" in get_str_tag(xml_link_element):
        # for definition networks we need to create both a physical and a logical network
        network_factories.append(PhysicalDefinitionNetworkFactory())
        network_factories.append(LogicalDefinitionNetworkFactory())
    elif "labelLink" in get_str_tag(xml_link_element):
        network_factories.append(LabelNetworkFactory())
    elif "referenceLink" in get_str_tag(xml_link_element):
        network_factories.append(ReferenceNetworkFactory())
    elif "footnoteLink" in get_str_tag(xml_link_element):
        network_factories.append(FootnoteNetworkFactory())
    else:
        raise NotImplementedError(
            f"the link element {xml_link_element.tag} is not supported"
        )

    for network_factory in network_factories:
        nodes_lookup: dict[str, list[INetworkNode]] = defaultdict(list)
        edges: set[tuple[str, str, str]] = set()
        node_to_arcs: dict[str, list[lxml.etree._Element]] = defaultdict(list)  # type: ignore
        roots: set[INetworkNode] = set()

        for arc_element in find_elements(xml_link_element, ".//*[@xlink:type='arc']"):
            arc_from = get_str_attribute(arc_element, "xlink:from")
            arc_to = get_str_attribute(arc_element, "xlink:to")
            arc_role = get_str_attribute(arc_element, "xlink:arcrole")

            if (arc_from, arc_to, arc_role) in edges:
                # the edge already exists. The SEC XBRL Filing Manual says that this is an error.
                raise ValueError(
                    f"the arc element with from='{arc_from}' and to='{arc_to}' is a duplicate"
                )

            edges.add((arc_from, arc_to, arc_role))
            node_to_arcs[arc_from].append(arc_element)
            node_to_arcs[arc_to].append(arc_element)

        for link_element in find_elements(
            xml_link_element, ".//*[@xlink:type='resource' or @xlink:type='locator']"
        ):
            if not isinstance(link_element, lxml.etree._Element):  # type: ignore
                raise TypeError(
                    f"the xpath query did not return a list of lxml.etree._Element."
                )

            label = get_str_attribute(link_element, "xlink:label")
            to_object: IResource | IReportElement | Fact = get_object_from_reference(
                link_element, context
            )
            node_arcs = node_to_arcs[label]
            arcs_to = list(
                filter(
                    lambda arc: get_str_attribute(arc, "xlink:to", "") == label,
                    node_arcs,
                )
            )
            arcs_from = list(
                filter(
                    lambda arc: get_str_attribute(arc, "xlink:from", "") == label,
                    node_arcs,
                )
            )

            if network_factory.is_physical():
                if len(arcs_to) == 0 and len(arcs_from) == 0:
                    node = network_factory.create_node(
                        xml_link_element, link_element, None, to_object
                    )
                    roots.add(node)
                    nodes_lookup[label].append(node)
                else:
                    outgoing_role_types = set(
                        get_str_attribute(arc, "xlink:arcrole") for arc in arcs_from
                    )

                    incoming_role_types = set(
                        get_str_attribute(arc, "xlink:arcrole") for arc in arcs_to
                    )

                    for role_type in incoming_role_types.union(outgoing_role_types):
                        node_arcs.sort(
                            key=lambda arc: get_str_attribute(arc, "xlink:to") == label,
                            reverse=True,
                        )

                        arc = next(
                            (
                                arc
                                for arc in node_arcs
                                if get_str_attribute(arc, "xlink:arcrole") == role_type
                            ),
                            None,
                        )

                        node = network_factory.create_node(
                            xml_link_element, link_element, arc, to_object
                        )

                        if role_type not in incoming_role_types:
                            roots.add(node)
                        nodes_lookup[label].append(node)

            else:
                if len(arcs_to) == 0 and len(arcs_from) == 0:
                    node = network_factory.create_node(
                        xml_link_element, link_element, None, to_object
                    )
                    roots.add(node)
                    nodes_lookup[label].append(node)
                else:
                    arc = arcs_to[0] if len(arcs_to) > 0 else arcs_from[0]

                    node = network_factory.create_node(
                        xml_link_element, link_element, arc, to_object
                    )

                    if len(arcs_to) == 0:
                        roots.add(node)
                    nodes_lookup[label].append(node)

        # second pass. Create the tree by iterating over the edges and adding the edge's 'to' node as a child to the edge's 'from' node
        for arc_from, arc_to, arc_role in edges:
            from_nodes = nodes_lookup[arc_from]
            to_nodes = nodes_lookup[arc_to]

            if network_factory.is_physical():
                from_nodes = list(
                    filter(lambda node: node.get_arc_role() == arc_role, from_nodes)
                )
                to_nodes = list(
                    filter(lambda node: node.get_arc_role() == arc_role, to_nodes)
                )

            for from_node, to_node in itertools.product(from_nodes, to_nodes):
                # Now we can link the nodes
                from_node._add_child(to_node)  # type: ignore

        # third pass. If the network is physical, create a network for each arcrole in the roots
        # if the network is logical (not physical), create a single network with all the roots
        # Networks have to be non-empty, so if there are no roots, we skip this step
        if len(roots) == 0:
            continue

        if network_factory.is_physical():
            role_types = set(node.get_arc_role() for node in roots)
            for role_type in role_types:
                role_type_roots = [
                    node for node in roots if node.get_arc_role() == role_type
                ]
                network = network_factory.create_network(
                    xml_link_element, role_type_roots
                )
                network_factory.update_report_elements(
                    context.get_report_element_repository(), network
                )
                networks.append(network)
        else:
            root_nodes = list(roots)
            network = network_factory.create_network(xml_link_element, root_nodes)
            network_factory.update_report_elements(
                context.get_report_element_repository(), network
            )
            networks.append(network)

    return networks
