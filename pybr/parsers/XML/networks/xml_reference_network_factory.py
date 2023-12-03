import lxml
import lxml.etree
from typing import cast
from pybr import QName
from pybr.networks import INetwork, INetworkNode, ReferenceNetworkNode, ReferenceNetwork
from pybr.reportelements import *
from pybr.resource import BrelReference

from .i_xml_network_factory import IXMLNetworkFactory

class ReferenceNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag)

        if not all(isinstance(root, ReferenceNetworkNode) for root in roots):
            raise TypeError("roots must all be of type ReferenceNetworkNode")
        
        if link_role is None:
            raise ValueError("link_role must not be None")
        
        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        
        roots_cast = cast(list[ReferenceNetworkNode], roots)
        
        return ReferenceNetwork(roots_cast, link_role, link_qname)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, points_to: IReportElement|BrelReference) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = float(xml_arc.attrib.get("order") or 1).__round__()
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

        return ReferenceNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, points_to: IReportElement|BrelReference) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = 0 # TODO: ask ghislain why this is different from the calculation network and definition network
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

        return ReferenceNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], network: INetwork) -> dict[QName, IReportElement]:
        """
        Definition networks do not change the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a DefinitionNetwork
        @return: dict[QName, IReportElement] containing all report elements. Some report elements might differ in type from the report_elements parameter
        """
        return report_elements
    
    def is_physical(self) -> bool:
        return True

