"""
This module contains the XMLDefinitionNetworkFactory class
XMLDefinitionNetworkFactories are used to create physical DefinitionNetworks from XML.
This module is usedc by the XML network parser to build physical definition networks.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 30 January 2024

====================
"""

from typing import cast, Mapping

import lxml
import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import (
    DefinitionNetwork,
    DefinitionNetworkNode,
    INetwork,
    INetworkNode,
)
from brel.parsers.utils import get_str
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.reportelements import *
from brel.resource import IResource


class PhysicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_qname = self._make_qname(xml_link.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link}")

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, self.is_physical())

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        label = get_str(xml_referenced_element, self._clark("xlink", "label"))

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0.0
            arc_qname = self._make_qname("link:unknown")
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = 0.0
            arc_qname = self._make_qname(xml_arc.tag)
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = float(xml_arc.attrib.get("order") or 0.0)
            arc_qname = self._make_qname(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

        return DefinitionNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)

    def update_report_elements(
        self, report_elements: Mapping[QName, IReportElement], network: INetwork
    ) -> Mapping[QName, IReportElement]:
        """
        Definition networks do not change the report elements
        :param report_elements: Mapping[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a DefinitionNetwork
        :return: Mapping[QName, IReportElement] containing all report elements. Some report elements might differ in type from the report_elements parameter
        """
        return report_elements

    def is_physical(self) -> bool:
        return True


class LogicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_qname = self._make_qname(xml_link.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link}")

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, self.is_physical())

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        label = get_str(xml_referenced_element, self._clark("xlink", "label"))

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0
            arc_qname = QName.from_string("link:unknown", self.get_qname_nsmap())
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = 0
            arc_qname = self._make_qname(xml_arc.tag)
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = float(xml_arc.attrib.get("order") or 0.0).__round__()
            arc_qname = self._make_qname(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

        return DefinitionNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)

    def update_report_elements(self, report_elements: Mapping[QName, IReportElement], network: INetwork):
        pass

    def is_physical(self) -> bool:
        return False
