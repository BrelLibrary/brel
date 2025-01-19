"""
This module contains the CalculationNetworkFactory class.
CalculationNetworkFactories are used to create CalculationNetworks from XML.
They are used by the XML parsers for networks to build calculation networks.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 19 February 2024

====================
"""

from typing import cast, Mapping

import lxml
import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import (
    CalculationNetwork,
    CalculationNetworkNode,
    INetwork,
    INetworkNode,
)
from brel.parsers.utils import get_str
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.reportelements import IReportElement
from brel.resource import IResource


class CalculationNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str(xml_link_element, self._clark("xlink", "role"), None)
        link_qname = self._make_qname(xml_link_element.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        if not all(isinstance(root, CalculationNetworkNode) for root in roots):
            raise TypeError("roots must all be of type CalculationNetworkNode")

        if link_role is None:
            raise ValueError("link_role must not be None")

        roots_cast = cast(list[CalculationNetworkNode], roots)

        return CalculationNetwork(roots_cast, link_role, link_qname, self.is_physical())

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
            weight = 0.0
            arc_role = "unknown"
            order: float = 1
            arc_qname = self._make_qname("link:unknown")
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            # the node is a root
            weight = 0.0
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = 1
            arc_qname = self._make_qname(xml_arc.tag)
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            weight = float(xml_arc.attrib.get("weight") or 0.0)
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = float(get_str(xml_arc, "order", "1.0"))
            arc_qname = self._make_qname(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

        # also, all calculation network nodes have to point to a concept
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type Concept, not {type(points_to)}")

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

    def update_report_elements(self, report_elements: Mapping[QName, IReportElement], _: INetwork):
        pass

    def is_physical(self) -> bool:
        return False
