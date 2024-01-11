"""
This module contains the XMLDefinitionNetworkFactory class
XMLDefinitionNetworkFactories are used to create physical DefinitionNetworks from XML.
This module is usedc by the XML network parser to build physical definition networks.

@author: Robin Schmidiger
@version: 0.4
@date: 04 January 2024
"""

import lxml
import lxml.etree
from typing import cast
from brel import QName, QNameNSMap, Fact
from brel.networks import (
    INetwork,
    INetworkNode,
    DefinitionNetworkNode,
    DefinitionNetwork,
)
from brel.reportelements import *
from brel.resource import IResource

from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils import get_str


class PhysicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = get_str(xml_link, f"{{{nsmap['xlink']}}}role")
        link_qname = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(
                f"linkrole attribute not found on link element {xml_link}"
            )

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, True)

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = get_str(xml_referenced_element, f"{{{nsmap['xlink']}}}label")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0.0
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = 0.0
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0)
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str(xml_link, "{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return DefinitionNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def update_report_elements(
        self, report_elements: dict[QName, IReportElement], network: INetwork
    ) -> dict[QName, IReportElement]:
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
    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(
                f"linkrole attribute not found on link element {xml_link}"
            )

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, False)

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = get_str(xml_referenced_element, f"{{{nsmap['xlink']}}}label")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = 0
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0).__round__()
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str(xml_link, "{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return DefinitionNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def update_report_elements(
        self, report_elements: dict[QName, IReportElement], network: INetwork
    ) -> dict[QName, IReportElement]:
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
