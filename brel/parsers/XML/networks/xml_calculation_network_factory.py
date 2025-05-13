"""
This module contains the CalculationNetworkFactory class.
CalculationNetworkFactories are used to create CalculationNetworks from XML.
They are used by the XML parsers for networks to build calculation networks.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 13 May 2025

====================
"""

from typing import cast

from lxml.etree import _Element  # type: ignore

from brel.brel_fact import Fact
from brel.networks import (
    CalculationNetwork,
    CalculationNetworkNode,
    INetwork,
    INetworkNode,
)
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import (
    qname_from_str,
    to_namespace_localname_notation,
)
from brel.reportelements import IReportElement
from brel.resource import IResource


class CalculationNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: _Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role"), None
        )
        link_qname = qname_from_str(xml_link.tag, xml_link)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        if not all(isinstance(root, CalculationNetworkNode) for root in roots):
            raise TypeError("roots must all be of type CalculationNetworkNode")

        roots_cast = cast(list[CalculationNetworkNode], roots)

        return CalculationNetwork(roots_cast, link_role, link_qname, self.is_physical())

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
            weight = 0.0
            arc_role = "unknown"
            order: float = 1
            arc_qname = qname_from_str("link:unknown", xml_link)
        elif get_str_attribute(xml_arc, "xlink:from") == label:
            # the node is a root
            weight = 0.0
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = 1
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif get_str_attribute(xml_arc, "xlink:to") == label:
            weight = float(xml_arc.attrib.get("weight") or 0.0)
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            order = float(get_str_attribute(xml_arc, "order", "1.0"))
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(xml_link, "xlink:role")
        link_name = qname_from_str(xml_link.tag, xml_link)

        link_role = get_str_attribute(xml_link, "xlink:role")
        link_name = qname_from_str(xml_link.tag, xml_link)

        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return CalculationNetworkNode(
            points_to,
            [],
            arc_role,
            arc_qname,
            link_role,
            link_name,
            weight,
            order,
        )

    def is_physical(self) -> bool:
        return False
