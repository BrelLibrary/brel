import lxml
import lxml.etree
from typing import cast
from pybr import QName
from pybr.networks import INetwork, INetworkNode, DefinitionNetworkNode, DefinitionNetwork
from pybr.reportelements import *

from .i_xml_network_factory import IXMLNetworkFactory

class PhysicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag)
        
        return DefinitionNetwork(roots, link_role, link_qname, True)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = float(xml_arc.attrib.get("order")).__round__()
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        return DefinitionNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, order)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = 0 # TODO: ask ghislain why this is different from the calculation network and definition network
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        return DefinitionNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, order)
    
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
        
        return DefinitionNetwork(roots, link_role, link_qname, False)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = float(xml_arc.attrib.get("order")).__round__()
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        return DefinitionNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, order)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = 0 # TODO: ask ghislain why this is different from the calculation network and definition network
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        return DefinitionNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, order)
    
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
        #     if "all" in arc_role and not isinstance(report_element, PyBRHypercube):
        #         print(f"Warning: report element {report_element.get_name()} is not a PyBRHypercube")
        #     elif "hypercube-dimension" in arc_role and not isinstance(report_element, PyBRDimension):
        #         print(f"Warning: report element {report_element.get_name()} is not a PyBRDimension")
        #     elif "dimension-domain" in arc_role and not isinstance(report_element, PyBRMember):
        #         print(f"Warning: report element {report_element.get_name()} is not a PyBRMember")
        #     elif "dimension-domain" in arc_role and not isinstance(report_element, PyBRMember):
        #         print(f"Warning: report element {report_element.get_name()} is not a PyBRMember")
        return report_elements
    
    def is_physical(self) -> bool:
        return False