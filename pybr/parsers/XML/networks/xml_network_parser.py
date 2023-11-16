import lxml.etree

from pybr import QName
from pybr.networks import *
from pybr.reportelements import *

from typing import cast

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory
from .xml_presentation_network_factory import PresentationNetworkFactory    
from .xml_calculation_network_factory import CalculationNetworkFactory    
from .xml_definition_network_factory import DefinitionNetworkFactory

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
        network_factory: IXMLNetworkFactory = CalculationNetworkFactory()
    elif xml_link_element.tag == f"{{{nsmap['link']}}}definitionLink":
        network_factory: IXMLNetworkFactory = DefinitionNetworkFactory()
    else:
        # raise ValueError(f"xml_link_element must be either a link:presentationLink or a link:calculationLink, not {xml_link_element.tag}")
        print(f"Warning: xml_link_element must be either a link:presentationLink or a link:calculationLink, not {xml_link_element.tag}")
        return None, report_elements
        
    
    def __get_report_element_from_loc_label(loc_label: str) -> IReportElement:
        """
        Get the report element from the loc label. The loc label is the xlink:label attribute of the link:loc element.
        @param loc_label: str containing the loc label
        @return: IReportElement
        """

        loc_xml = xml_link_element.find(f".//link:loc[@{{{nsmap['xlink']}}}label='{loc_label}']", namespaces=nsmap)

        href = loc_xml.get(f"{{{nsmap['xlink']}}}href")
        report_element_qname = __get_qname_from_href(href)
        return report_elements[report_element_qname]
        

    nodes_map : dict[str, INetworkNode] = {}
    edges: list[tuple[str, str]] = []

    # first get all link:presentationArc elements
    # get all elements with @xlink:type="arc"
    xml_arcs = xml_link_element.findall(f".//*[@xlink:type='arc']", namespaces=nsmap)

    for xml_arc in xml_arcs:
        # find the xlink:from and xlink:to attributes
        loc_label_from = xml_arc.get(f"{{{nsmap['xlink']}}}from")
        loc_label_to = xml_arc.get(f"{{{nsmap['xlink']}}}to")

        report_element = __get_report_element_from_loc_label(loc_label_to)

        # create the nodes
        # node_to = internal_node_factory(xml_arc, report_element)
        node_to = network_factory.create_internal_node(xml_arc, report_element)

        # add the node to the nodemap and the edge to the edges list
        # this will is used to link the nodes into a tree in the next pass
        nodes_map[loc_label_to] = node_to
        edges.append((loc_label_from, loc_label_to))
    
    # second pass over all nodes to link them together. Also find the root node
    roots = []
    for loc_label_from, loc_label_to in edges:

        from_node = nodes_map.get(loc_label_from, None)
        to_node = nodes_map.get(loc_label_to, None)

        if from_node is None:
            xml_arc = xml_link_element.find(f".//*[@{{{nsmap['xlink']}}}from='{loc_label_from}']", namespaces=nsmap)
            report_element = __get_report_element_from_loc_label(loc_label_from)
            from_node = network_factory.create_root_node(xml_arc, report_element)
            nodes_map[loc_label_from] = from_node
            roots.append(from_node)

        from_node.add_child(to_node)
        
    if len(roots) > 0: 
        network = network_factory.create_network(xml_link_element, roots)
        report_elements = network_factory.update_report_elements(report_elements, network)
    
        return network, report_elements
    
    else:
        return None, report_elements
