import lxml
import lxml.etree
from typing import cast
from pybr import QName
from pybr.networks import INetwork, INetworkNode, CalculationNetwork, CalculationNetworkNode
from pybr.reportelements import IReportElement

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory

class CalculationNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link_element.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        
        if not all(isinstance(root, CalculationNetworkNode) for root in roots):
            raise TypeError("roots must all be of type CalculationNetworkNode")
        
        if link_role is None:
            raise ValueError("link_role must not be None")

        roots_cast = cast(list[CalculationNetworkNode], roots)

        return CalculationNetwork(roots_cast, link_role, link_qname)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        weight = float(xml_arc.attrib.get("weight") or 0.0)
        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = int(xml_arc.attrib.get("order") or 1)
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")

        return CalculationNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, weight, order)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        weight = 0.0
        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = 1
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")

        return CalculationNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, weight, order)
    
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