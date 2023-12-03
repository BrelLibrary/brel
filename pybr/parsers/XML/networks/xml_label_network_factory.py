import lxml
import lxml.etree
from typing import cast
from pybr import QName
from pybr.networks import INetwork, INetworkNode, LabelNetwork, LabelNetworkNode
from pybr.reportelements import IReportElement
from pybr.resource import BrelLabel

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory

class LabelNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link_element.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, LabelNetworkNode) for root in roots):
            raise TypeError("roots must all be of type LabelNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link_element}")
        
        roots_cast = cast(list[LabelNetworkNode], roots)

        return LabelNetwork(roots_cast, link_role, link_qname)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, points_to: IReportElement|BrelLabel) -> INetworkNode:
        
        if not isinstance(points_to, BrelLabel):
            raise TypeError(f"report_element must be of type BrelLabel, not {type(points_to)}")
        
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
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
        
        return LabelNetworkNode(points_to, arc_role, arc_qname, link_role, link_name)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, points_to: IReportElement|BrelLabel) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
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

        return LabelNetworkNode(points_to, arc_role, arc_qname, link_role, link_name)
    
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