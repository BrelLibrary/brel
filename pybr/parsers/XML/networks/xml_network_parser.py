import lxml.etree

from pybr import QName
from pybr.networks import *
from pybr.reportelements import *

from typing import cast
from collections import defaultdict

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory
from .xml_presentation_network_factory import PresentationNetworkFactory    
from .xml_calculation_network_factory import CalculationNetworkFactory    
from .xml_definition_network_factory import DefinitionNetworkFactory
from .xml_label_network_factory import LabelNetworkFactory
from .xml_reference_network_factory import ReferenceNetworkFactory

def __get_qname_from_href(href: str) -> QName:
    """
    Get a QName from an href attribute
    @param href: str containing the href attribute
    @param nsmap: dict[str, str] containing the namespace map
    @return: QName
    """
    # TODO: this feels like a hack
    # generate the qname from the href
    # Step 1. take the stuff after the #
    # Step 2. replace the _ with :
    # Step 3. parse the string as a QName
    href = href.split("#")[1]
    href = href.replace("_", ":")
    report_element_qname = QName.from_string(href)
    return report_element_qname

def networks_from_xmls(
        xml_trees: list[lxml.etree._ElementTree],
        report_elements: dict[QName, IReportElement]
        ) -> dict[str, list[INetwork]]:
    
    nsmap = QName.get_nsmap()

    networks: dict[str, list[INetwork]] = defaultdict(list)

    def link_to_component_name(link: lxml.etree._Element) -> str:
        """
        Given a link element, get the component name.
        @param link: The link element.
        @return: The component name as a string.
        @raise ValueError: If the roleRef cannot be found or if the roleRef has either no href attribute or an invalid href attribute.
        """

        link_role = link.get("{" + nsmap["xlink"] + "}role")

        if link_role is None:
            raise ValueError("the link element does not have a xlink:role attribute")
        
        # TODO: TODO: think about this
        if "/role/link" in link_role:
            return "labels_networks" 

        role_ref = xml_tree.find(f".//link:roleRef[@roleURI='{link_role}']", namespaces=nsmap)
        if role_ref is None:
            raise ValueError(f"the roleRef with roleURI='{link_role}' could not be found")
        
        href = role_ref.get("{" + nsmap["xlink"] + "}href")
        if href is None:
            raise ValueError(f"the roleRef with roleURI='{link_role}' does not have a href attribute")
        _, component_name = href.split("#")

        if component_name == "":
            raise ValueError(f"the roleRef with roleURI='{link_role}' has an invalid href attribute href='{href}'")

        return component_name

    for xml_tree in xml_trees:
        
        # check if root is a linkbase
        root = xml_tree.getroot()
        if root.tag == f"{{{nsmap['link']}}}linkbase":
            xml_links = root.findall("link:*[@xlink:role]", namespaces=nsmap)
        else:
            xml_links = xml_tree.findall(".//link:linkbase/*[@xlink:role]", namespaces=nsmap)
            if len(xml_links) > 0:
                print("WARNING: found non-root linkbase")

        for xml_link in xml_links:
            # parse the network and update the report elements
            network, report_elements = network_from_xml(xml_link, report_elements)

            if network is not None:
                # get the component name
                component_name = link_to_component_name(xml_link)

                # add the presentation network to the networks dict
                networks[component_name].append(network)
    
    return networks
    

def network_from_xml(xml_link_element: lxml.etree._Element, report_elements: dict[QName, IReportElement]) -> tuple[INetwork, dict[QName, IReportElement]] | tuple[None, dict[QName, IReportElement]]:
    """
    Create a Network from an lxml.etree._Element. Note that this method also returns a dict containing all report elements.
    This is because networks may change the internal representation of the report elements. More specifically, it may promote
    abstracts to line items.
    @param xml_element: lxml.etree._Element to be parsed. This element must be a child of a link:linkbase element and must have a xlink:role attribute.
    @param component: PyBRComponent to which the network belongs.
    @return: An instance of INetwork. can be either a PresentationNetwork, CalculationNetwork, or any other kind of network.
    """
    nsmap = QName.get_nsmap()

    if xml_link_element.tag == f"{{{nsmap['link']}}}presentationLink":
        network_factory: IXMLNetworkFactory = PresentationNetworkFactory()
    elif xml_link_element.tag == f"{{{nsmap['link']}}}calculationLink":
        network_factory = CalculationNetworkFactory()
    elif xml_link_element.tag == f"{{{nsmap['link']}}}definitionLink":
        network_factory = DefinitionNetworkFactory()
    elif xml_link_element.tag == f"{{{nsmap['link']}}}labelLink":
        network_factory = LabelNetworkFactory()
    elif xml_link_element.tag == f"{{{nsmap['link']}}}referenceLink":
        network_factory = ReferenceNetworkFactory()
    else:
        # raise ValueError(f"xml_link_element must be either a link:presentationLink or a link:calculationLink, not {xml_link_element.tag}")
        print(f"Warning: xml_link_element must be either a link:presentationLink or a link:calculationLink, not {xml_link_element.tag}")
        return None, report_elements
        
    
    def get_report_element_from_locator(locator_xml: lxml.etree._Element) -> IReportElement:
        """
        Get the report element from the loc label. The loc label is the xlink:label attribute of the link:loc element.
        @param loc_label: str containing the loc label
        @return: IReportElement if the report element exists. None otherwise.
        """

        # get the xlink:loc attribute
        if locator_xml.get(f"{{{nsmap['xlink']}}}type", "") != "locator":
            raise ValueError(f"the locator_xml element {locator_xml.tag} does not have a xlink:type attribute with value 'locator'")

        href = locator_xml.get(f"{{{nsmap['xlink']}}}href")
        report_element_qname = __get_qname_from_href(href)
        return report_elements[report_element_qname]
        

    nodes_map : dict[str, INetworkNode] = {}
    edges: list[tuple[str, str]] = []

    # first get all link:presentationArc elements
    # get all elements with @xlink:type="arc"
    xml_arcs = xml_link_element.findall(f".//*[@xlink:type='arc']", namespaces=nsmap)

    for xml_arc in xml_arcs:
        # find the xlink:from and xlink:to attributes
        arc_from = xml_arc.get(f"{{{nsmap['xlink']}}}from")
        arc_to = xml_arc.get(f"{{{nsmap['xlink']}}}to")

        if arc_from is None or arc_to is None:
            raise ValueError("xlink:from and xlink:to must be present on all xlink:type='arc' elements")
        
        referenced_element = xml_link_element.find(f".//*[@{{{nsmap['xlink']}}}label='{arc_to}']", namespaces=nsmap)

        if referenced_element is None:
            raise ValueError(f"the element with xlink:label='{arc_to}' could not be found")
        
        referenced_element_type = referenced_element.get(f"{{{nsmap['xlink']}}}type", "")

        to_element = None

        if referenced_element_type == "locator":
            to_element = get_report_element_from_locator(referenced_element)
        elif referenced_element_type == "resource":
            # TODO: implement resources
            pass
        


        # create the nodes
        # node_to = internal_node_factory(xml_arc, report_element)
        if to_element is not None:
            node_to = network_factory.create_internal_node(xml_arc, to_element)

            # add the node to the nodemap and the edge to the edges list
            # this will is used to link the nodes into a tree in the next pass
            nodes_map[arc_to] = node_to
        edges.append((arc_from, arc_to))
    
    # second pass over all nodes to link them together. Also find the root node
    roots = []
    for arc_from, arc_to in edges:

        from_node = nodes_map.get(arc_from, None)
        to_node = nodes_map.get(arc_to, None)

        if from_node is None:
            xml_arc = xml_link_element.find(f".//*[@{{{nsmap['xlink']}}}from='{arc_from}']", namespaces=nsmap)
            referenced_element = xml_link_element.find(f".//*[@{{{nsmap['xlink']}}}label='{arc_from}']", namespaces=nsmap)
            report_element = get_report_element_from_locator(referenced_element)
            from_node = network_factory.create_root_node(xml_arc, report_element)
            nodes_map[arc_from] = from_node
            roots.append(from_node)
        
        if to_node is not None:
            from_node.add_child(to_node)
        
    if len(roots) > 0: 
        network = network_factory.create_network(xml_link_element, roots)
        report_elements = network_factory.update_report_elements(report_elements, network)
    
        return network, report_elements
    
    else:
        return None, report_elements
