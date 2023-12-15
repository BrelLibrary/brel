import lxml
import lxml.etree
from typing import cast
from brel import QName, QNameNSMap
from brel.networks import INetwork, INetworkNode, FootnoteNetworkNode, FootnoteNetwork
from brel.reportelements import *
from brel.reportelements import IReportElement
from brel.resource import IResource, BreelFootnote

from .i_xml_network_factory import IXMLNetworkFactory

class FootnoteNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)
    
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if not all(isinstance(root, FootnoteNetworkNode) for root in roots):
            raise TypeError("roots must all be of type FootnoteNetworkNode")
        
        if link_role is None:
            raise ValueError("link_role must not be None")
        
        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        
        roots_cast = cast(list[FootnoteNetworkNode], roots)

        return FootnoteNetwork(roots_cast, link_role, link_qname)
    
    def create_node(
            self, 
            xml_link: lxml.etree._Element, 
            xml_referenced_element: lxml.etree._Element, 
            xml_arc: lxml.etree._Element | None, 
            points_to: IReportElement | IResource
            ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(f"label attribute not found on referenced element {xml_referenced_element}")
        
        if xml_arc is None:
            # the node is not connected to any other node
            arc_role: str | bytes | None = "unknown"
            order = 1.0
            arc_qname = QName.from_string("link:unknown", self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = 1.0
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 1)
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if isinstance(arc_role, bytes):
            arc_role = arc_role.decode()
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")
        
        if isinstance(points_to, IResource) and not isinstance(points_to, BreelFootnote):
            raise ValueError(f"points_to must be of type BreelFootnote, not {type(points_to)}")
        
        return FootnoteNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], network: INetwork) -> dict[QName, IReportElement]:
        return report_elements
    
    def is_physical(self) -> bool:
        return True

        