import lxml
import lxml.etree
from typing import cast
from brel import QName
from brel.networks import INetwork, INetworkNode, ReferenceNetworkNode, ReferenceNetwork
from brel.reportelements import *
from brel.resource import BrelReference, IResource

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
    
    def create_node(self, xml_link: lxml.etree._Element, xml_referenced_element: lxml.etree._Element, xml_arc: lxml.etree._Element | None, points_to: IReportElement|IResource) -> INetworkNode:
        nsmap = QName.get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(f"label attribute not found on referenced element {xml_referenced_element}")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 1.0
            arc_qname = QName.from_string("link:unknown")
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = 1.0 # TODO: ask ghislain why this is different from the calculation network and definition network
            arc_qname = QName.from_string(xml_arc.tag)
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 1)
            arc_qname = QName.from_string(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

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

        if isinstance(points_to, IResource) and not isinstance(points_to, BrelReference):
            raise TypeError(f"When creating a reference network, if points_to is an IResource, it must be of type BrelReference, not {type(points_to)}")

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

