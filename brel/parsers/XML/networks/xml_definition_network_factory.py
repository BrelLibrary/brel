import lxml
import lxml.etree
from typing import cast
from brel import QName
from brel.networks import INetwork, INetworkNode, DefinitionNetworkNode, DefinitionNetwork
from brel.reportelements import *
from brel.resource import IResource

from .i_xml_network_factory import IXMLNetworkFactory

class PhysicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link}")
        
        roots_cast = cast(list[DefinitionNetworkNode], roots)
        
        return DefinitionNetwork(roots_cast, link_role, link_qname, True)
    
    def create_node(self, xml_link: lxml.etree._Element, xml_referenced_element: lxml.etree._Element, xml_arc: lxml.etree._Element | None, points_to: IReportElement|IResource) -> INetworkNode:
        nsmap = QName.get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(f"label attribute not found on referenced element {xml_referenced_element}")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0
            arc_qname = QName.from_string("link:unknown")
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = 0 # TODO: ask ghislain why this is different from the calculation network and definition network
            arc_qname = QName.from_string(xml_arc.tag)
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0).__round__()
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
        
        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

        return DefinitionNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)
    
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

class LogicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link}")
        
        roots_cast = cast(list[DefinitionNetworkNode], roots)
        
        return DefinitionNetwork(roots_cast, link_role, link_qname, False)
    
    def create_node(self, xml_link: lxml.etree._Element, xml_referenced_element: lxml.etree._Element, xml_arc: lxml.etree._Element | None, points_to: IReportElement|IResource) -> INetworkNode:
        nsmap = QName.get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(f"label attribute not found on referenced element {xml_referenced_element}")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0
            arc_qname = QName.from_string("link:unknown")
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = 0 # TODO: ask ghislain why this is different from the calculation network and definition network
            arc_qname = QName.from_string(xml_arc.tag)
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0).__round__()
            arc_qname = QName.from_string(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        # check if the arc role is valid
        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        
        # check if the link role is valid
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")
        
        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

        return DefinitionNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], network: INetwork) -> dict[QName, IReportElement]:
        """
        Definition networks do not change the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a DefinitionNetwork
        @return: dict[QName, IReportElement] containing all report elements. Some report elements might differ in type from the report_elements parameter
        """
        # TODO: Implement
        # for node in network.get_all_nodes():
        #     arc_role = node.get_arc_role()
        #     report_element = node.get_report_element()
        #     if "all" in arc_role and not isinstance(report_element, Hypercube):
        #         print(f"Warning: report element {report_element.get_name()} is not a Hypercube")
        #     elif "hypercube-dimension" in arc_role and not isinstance(report_element, Dimension):
        #         print(f"Warning: report element {report_element.get_name()} is not a Dimension")
        #     elif "dimension-domain" in arc_role and not isinstance(report_element, Member):
        #         print(f"Warning: report element {report_element.get_name()} is not a Member")
        #     elif "dimension-domain" in arc_role and not isinstance(report_element, Member):
        #         print(f"Warning: report element {report_element.get_name()} is not a Member")
        return report_elements
    
    def is_physical(self) -> bool:
        return False