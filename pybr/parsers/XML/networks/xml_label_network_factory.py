import lxml
import lxml.etree
from typing import cast
from pybr import QName
from pybr.networks import INetwork, INetworkNode, LabelNetwork, LabelNetworkNode
from pybr.reportelements import IReportElement

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory

class LabelNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link_element.tag)

        return LabelNetwork(roots, link_role, link_qname)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        raise NotImplementedError("Label networks do not have internal nodes")
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        return LabelNetworkNode(report_element, arc_role, arc_qname, link_role, link_name)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], _: INetwork) -> dict[QName, IReportElement]:
        """
        Calculation networks do not change the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a CalculationNetwork
        @return: dict[QName, IReportElement] containing all report elements. same as the report_elements parameter
        """
        return report_elements
    
    def is_physical(self) -> bool:
        return True