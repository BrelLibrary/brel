"""
This module contains the XMLDefinitionNetworkFactory class
XMLDefinitionNetworkFactories are used to create physical DefinitionNetworks from XML.
This module is usedc by the XML network parser to build physical definition networks.

====================

- author: Robin Schmidiger
- version: 0.8
- date: 12 May 2025

====================
"""

from typing import cast

from lxml.etree import _Element  # type: ignore

from brel.brel_fact import Fact
from brel.networks import (
    DefinitionNetwork,
    DefinitionNetworkNode,
    INetwork,
    INetworkNode,
)
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import (
    qname_from_str,
    to_namespace_localname_notation,
)
from brel.reportelements import *
from brel.resource import IResource
from brel.data.report_element.report_element_repository import ReportElementRepository


class PhysicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: _Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str_attribute(xml_link, "xlink:role")
        link_qname = qname_from_str(xml_link.tag, xml_link)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, self.is_physical())

    def create_node(
        self,
        xml_link: _Element,
        xml_referenced_element: _Element,
        xml_arc: _Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        label = get_str_attribute(xml_referenced_element, "xlink:label")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0.0
            arc_qname = qname_from_str("link:unknown", xml_link)
        elif get_str_attribute(xml_arc, "xlink:from") == label:
            # the node is a root
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = 0.0
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif get_str_attribute(xml_arc, "xlink:to", None) == label:
            # the node is an inner node
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0)
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role")
        )
        link_name = qname_from_str(xml_link.tag, xml_link)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return DefinitionNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def update_report_elements(
        self, report_element_repository: ReportElementRepository, network: INetwork
    ):
        """
        Definition networks do not change the report elements
        :param report_elements: Mapping[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a DefinitionNetwork
        :return: Mapping[QName, IReportElement] containing all report elements. Some report elements might differ in type from the report_elements parameter
        """
        pass

    def is_physical(self) -> bool:
        return True


class LogicalDefinitionNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: _Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str_attribute(xml_link, "xlink:role")
        link_qname = qname_from_str(xml_link.tag, xml_link)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, DefinitionNetworkNode) for root in roots):
            raise TypeError("roots must all be of type DefinitionNetworkNode")

        roots_cast = cast(list[DefinitionNetworkNode], roots)

        return DefinitionNetwork(roots_cast, link_role, link_qname, self.is_physical())

    def create_node(
        self,
        xml_link: _Element,
        xml_referenced_element: _Element,
        xml_arc: _Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        label = get_str_attribute(xml_referenced_element, "xlink:label")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 0
            arc_qname = qname_from_str("link:unknown", xml_link)
        elif get_str_attribute(xml_arc, "xlink:from") == label:
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = 0
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif get_str_attribute(xml_arc, "xlink:to") == label:
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = float(xml_arc.attrib.get("order") or 0.0).__round__()
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(xml_link, "xlink:role")
        link_name = qname_from_str(xml_link.tag, xml_link)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return DefinitionNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def is_physical(self) -> bool:
        return False
