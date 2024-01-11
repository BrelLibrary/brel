"""
This module parses XML extended links into one or multiple networks.
Networks are covered in the XBRL Generic Links spec.
https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html

@author: Robin Schmidiger
@version: 0.14
@date: 2023-12-19
"""


import lxml.etree
import itertools

from brel import QName, QNameNSMap, Fact
from brel.networks import *
from brel.reportelements import *
from brel.resource import *
from brel.parsers import XMLFileManager

from typing import cast, Any
from collections import defaultdict

from brel.parsers.XML.networks import (
    IXMLNetworkFactory,
    PresentationNetworkFactory,
    CalculationNetworkFactory,
    PhysicalDefinitionNetworkFactory,
    LogicalDefinitionNetworkFactory,
    LabelNetworkFactory,
    ReferenceNetworkFactory,
    FootnoteNetworkFactory,
)


def get_object_from_reference(
    referenced_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    id_to_any: dict[str, Any],
) -> IResource | IReportElement | Fact:
    """
    Given a locator or resource element, get the object that the reference points to.
    :param referenced_element: The locator or resource element.
    :param qname_nsmap: The QNameNSMap of the filing.
    :param id_to_any: A dict mapping xml ids to report elements and resources.
    :returns: The object that the reference points to.
    :rtype: IResource|IReportElement|Fact
    :raises ValueError: If the referenced element does not have a xlink:type attribute with value 'locator' or 'resource'.
    """

    nsmap = qname_nsmap.get_nsmap()
    referenced_element_type = referenced_element.get(
        f"{{{nsmap['xlink']}}}type", ""
    )

    if referenced_element_type == "locator":
        # if the referenced element is a locator, get the referenced element from the report elements
        if (
            referenced_element.get(f"{{{nsmap['xlink']}}}type", "")
            != "locator"
        ):
            raise ValueError(
                f"the locator_xml element {referenced_element.tag} does not have a xlink:type attribute with value 'locator'"
            )

        to_element: IReportElement | IResource | Fact | None = None

        # get the href attribute
        href = cast(
            str, referenced_element.get(f"{{{nsmap['xlink']}}}href", "")
        )

        if "#" in href:
            _, elem_id = href.split("#")
        else:
            elem_id = href

        if elem_id not in id_to_any:
            raise ValueError(
                f"the referenced element {elem_id} could not be found"
            )
        report_element = id_to_any[elem_id]

        to_element = report_element

    elif referenced_element_type == "resource":
        # if the referenced element is a resource, create a new resource
        if referenced_element.tag == f"{{{nsmap['link']}}}label":
            to_element = BrelLabel.from_xml(referenced_element, qname_nsmap)
        elif referenced_element.tag == f"{{{nsmap['link']}}}reference":
            to_element = BrelReference.from_xml(
                referenced_element, qname_nsmap
            )
        elif referenced_element.tag == f"{{{nsmap['link']}}}footnote":
            to_element = BrelFootnote.from_xml(referenced_element, qname_nsmap)
        else:
            raise NotImplementedError(
                f"the referenced element {referenced_element.tag} is not supported"
            )
    else:
        raise NotImplementedError(
            f"the referenced element type {referenced_element_type} is not supported"
        )

    if to_element is None:
        raise ValueError(
            f"the referenced element {referenced_element} could not be found"
        )

    return to_element


def parse_xml_link(
    xml_link_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    id_to_any: dict[str, Any],
    report_elements: dict[QName, IReportElement],
) -> tuple[list[INetwork], dict[QName, IReportElement]]:
    """
    Parse an xml link element into one or multiple networks.
    :param xml_link_element: The xml link element to parse.
    :param qname_nsmap: The QNameNSMap of the filing.
    :param id_to_any: A dict mapping xml ids to report elements and resources.
    :param report_elements: A dict mapping QNames to report elements.
    :returns: A tuple containing a list of networks and a dict mapping QNames to report elements.
    :rtype: tuple[list[INetwork], dict[QName, IReportElement]]
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
        raise NotImplementedError(
            f"the link element {xml_link_element.tag} is not supported"
        )

    for network_factory in network_factories:
        nodes_lookup: dict[str, list[INetworkNode]] = defaultdict(list)
        edges: set[tuple[str, str]] = set()
        root_names: set[str] = set()

        # first pass. Iterate over all elements in the linkbase, create the nodes and edges
        link_children = xml_link_element.findall(".//*", namespaces=nsmap)
        if len(link_children) == 0:
            continue

        for link_child in link_children:
            child_type = link_child.get(f"{{{nsmap['xlink']}}}type", "")

            # for arcs, create the edges
            if child_type == "arc":
                xml_arc = link_child
                arc_from = xml_arc.get(f"{{{nsmap['xlink']}}}from")
                arc_to = xml_arc.get(f"{{{nsmap['xlink']}}}to")

                # check if the arc has a from and to attribute and if they are strings
                if arc_from is None:
                    raise ValueError(
                        f"the arc element {xml_arc.tag} does not have a xlink:from attribute"
                    )
                if not isinstance(arc_from, str):
                    raise TypeError(
                        f"the xlink:from attribute on the arc element {xml_arc.tag} is not a string"
                    )
                if arc_to is None:
                    raise ValueError(
                        f"the arc element {xml_arc.tag} does not have a xlink:to attribute"
                    )
                if not isinstance(arc_to, str):
                    raise TypeError(
                        f"the xlink:to attribute on the arc element {xml_arc.tag} is not a string"
                    )

                if (arc_from, arc_to) in edges:
                    # the edge already exists. The SEC XBRL Filing Manual says that this is an error.
                    raise ValueError(
                        f"the arc element with from='{arc_from}' and to='{arc_to}' is a duplicate"
                    )

                edges.add((arc_from, arc_to))

            # for resources and locators, create the nodes
            elif child_type == "resource" or child_type == "locator":
                xml_resource = link_child
                label = xml_resource.get(f"{{{nsmap['xlink']}}}label", None)
                if label is None:
                    raise ValueError(
                        f"the resource/locator element {xml_resource.tag} does not have a xlink:label attribute"
                    )
                if not isinstance(label, str):
                    raise TypeError(
                        f"the xlink:label attribute on the resource/locator element {xml_resource.tag} is not a string"
                    )

                to_object = get_object_from_reference(
                    xml_resource, qname_nsmap, id_to_any
                )

                # try finding an arc where 'to' points to the current resource/locator
                xpath_query = (
                    f".//*[@xlink:to='{label}' and @xlink:type='arc']"
                )
                arcs_to = xml_link_element.xpath(xpath_query, namespaces=nsmap)
                if not isinstance(arcs_to, list):
                    raise TypeError(
                        f"the xpath query {xpath_query} did not return a list"
                    )

                # if no arc is found, try again, but look for an arc with 'from' pointing to the current resource/locator
                xpath_query = (
                    f".//*[@xlink:from='{label}' and @xlink:type='arc']"
                )
                arcs_from = xml_link_element.xpath(
                    xpath_query, namespaces=nsmap
                )
                if not isinstance(arcs_from, list):
                    raise TypeError(
                        f"the xpath query {xpath_query} did not return a list"
                    )

                # think of to arcs as all edges pointing to a node and from arcs as all edges pointing from a node.
                # there should be at most one to arc because in XBRL all networks are trees.
                if len(arcs_to) == 0 and len(arcs_from) == 0:
                    # the node is not connected to any other node. The network only contains this node
                    node = network_factory.create_node(
                        xml_link_element, xml_resource, None, to_object
                    )
                    root_names.add(label)
                elif len(arcs_to) == 0:
                    # there is a from arc pointing from the node. This means that the node is a root node
                    if not isinstance(arcs_from[0], lxml.etree._Element):
                        raise TypeError(
                            f"the xpath query {xpath_query} did not return a list of lxml.etree._Element"
                        )
                    node = network_factory.create_node(
                        xml_link_element, xml_resource, arcs_from[0], to_object
                    )
                    root_names.add(label)
                else:
                    # there is a to arc pointing to the node. This means that the node is an inner node
                    if not isinstance(arcs_to[0], lxml.etree._Element):
                        raise TypeError(
                            f"the xpath query {xpath_query} did not return a list of lxml.etree._Element"
                        )
                    node = network_factory.create_node(
                        xml_link_element, xml_resource, arcs_to[0], to_object
                    )

                nodes_lookup[label].append(node)
            else:
                # TODO: add support for other types of elements in links.
                pass

        # second pass. Create the tree by
        roots: set[tuple[str, INetworkNode]] = set()
        for arc_from, arc_to in edges:
            from_nodes = nodes_lookup[arc_from]
            to_nodes = nodes_lookup[arc_to]

            for from_node, to_node in itertools.product(from_nodes, to_nodes):
                # if the from node is a root node, add it to the roots list
                if arc_from in root_names:
                    roots.add((arc_from, from_node))

                if (
                    network_factory.is_physical()
                    and from_node.get_arc_role() != to_node.get_arc_role()
                ):
                    # in this case, the 'from' node is a root node, since it has a different arcrole than the 'to' node
                    # Note that is only true for physical networks. Logical networks don't care if the arcroles are different
                    # first, we try to find a root node in roots that has the same arcrole as the 'to' node
                    def filter_func(root: tuple[str, INetworkNode]):
                        return (
                            root[1].get_arc_role() == to_node.get_arc_role()
                            and root[0] == arc_from
                        )

                    # for some reason this does not typecheck, even though it should.
                    # Seems to be an open issue with mypy (https://github.com/python/mypy/issues/12682)
                    root_name_node_pair: tuple[str, INetworkNode] | None = next(filter(filter_func, roots), None)  # type: ignore

                    # if not found, we create a new root node
                    if root_name_node_pair is None:
                        # query an arc with the same arcrole as the 'to' node.
                        # it also has to have the same 'from' and 'to' attributes as the current arc
                        xpath_query = f".//*[@xlink:from='{arc_from}'"
                        xpath_query += f" and @xlink:to='{arc_to}'"
                        xpath_query += (
                            f" and @xlink:arcrole='{to_node.get_arc_role()}'"
                        )
                        xpath_query += "]"
                        xml_arcs = xml_link_element.xpath(
                            xpath_query, namespaces=nsmap
                        )

                        # check if you found such an arc
                        if not isinstance(xml_arcs, list):
                            raise TypeError(
                                f"the xpath query {xpath_query} did not return a list"
                            )
                        if len(xml_arcs) == 0:
                            raise ValueError(
                                f"the xpath query {xpath_query} did not return any elements"
                            )
                        if not isinstance(xml_arcs[0], lxml.etree._Element):
                            raise TypeError(
                                f"the xpath query {xpath_query} did not return a list of lxml.etree._Element"
                            )

                        xml_arc = cast(lxml.etree._Element, xml_arcs[0])

                        # get the element the arc points to
                        referenced_element = xml_link_element.find(
                            f".//*[@{{{nsmap['xlink']}}}label='{arc_from}']",
                            namespaces=nsmap,
                        )
                        referenced_element = cast(
                            lxml.etree._Element, referenced_element
                        )
                        to_object = get_object_from_reference(
                            referenced_element, qname_nsmap, id_to_any
                        )

                        # create the root node
                        root_node = network_factory.create_node(
                            xml_link_element,
                            referenced_element,
                            xml_arc,
                            to_object,
                        )
                        root_name_node_pair = (arc_from, root_node)

                        # add the root node to the roots list
                        roots.add(root_name_node_pair)
                    # update the from_node
                    from_node = root_name_node_pair[1]

                # Now we can link the nodes
                from_node._add_child(to_node)

        # third pass. If the network is physical, create a network for each arcrole in the roots
        # if the network is logical (not physical), create a single network with all the roots
        # Networks have to be non-empty, so if there are no roots, we skip this step
        if len(roots) == 0:
            continue

        if network_factory.is_physical():
            present_arc_roles = set(
                map(lambda root: root[1].get_arc_role(), roots)
            )
            for arc_role in present_arc_roles:
                # filter the roots by arcrole

                # Note: could be done with lambas, but my typechecker is acting up, so I write everything out and typecheck by hand.
                def filter_func(root: tuple[str, INetworkNode]) -> bool:  # type: ignore
                    return root[1].get_arc_role() == arc_role

                def map_func(root: tuple[str, INetworkNode]) -> INetworkNode:
                    return root[1]

                arc_role_name_root_pairs = list(filter(filter_func, roots))
                arc_role_roots = list(map(map_func, arc_role_name_root_pairs))
                # create the network
                if len(arc_role_roots) == 0:
                    continue

                network = network_factory.create_network(
                    xml_link_element, arc_role_roots
                )
                # update the report elements
                report_elements = network_factory.update_report_elements(
                    report_elements, network
                )
                # add the network to the networks list
                networks.append(network)
        else:
            # create a network with all the roots
            root_nodes = list(map(lambda root: root[1], roots))
            network = network_factory.create_network(
                xml_link_element, root_nodes
            )
            # update the report elements
            report_elements = network_factory.update_report_elements(
                report_elements, network
            )
            # add the network to the networks list
            networks.append(network)

    return networks, report_elements
