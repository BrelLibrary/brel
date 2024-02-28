"""
This module contains the ReferenceNetworkFactory class.
ReferenceNetworkFactories are used to create ReferenceNetworks from XML.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 30 January 2024

====================
"""

from typing import cast, Mapping, Callable

import lxml
import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import (
    INetwork,
    INetworkNode,
    ReferenceNetwork,
    ReferenceNetworkNode,
)
from brel.parsers.utils import get_str
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.reportelements import *
from brel.resource import BrelReference, IResource


class ReferenceNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_qname = self._make_qname(xml_link.tag)

        if not all(isinstance(root, ReferenceNetworkNode) for root in roots):
            raise TypeError("roots must all be of type ReferenceNetworkNode")

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        roots_cast = cast(list[ReferenceNetworkNode], roots)

        return ReferenceNetwork(roots_cast, link_role, link_qname, self.is_physical())

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = get_str(xml_referenced_element, self._clark("xlink", "label"))

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 1.0
            arc_qname = self._make_qname("link:unknown")
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = 1.0
            arc_qname = self._make_qname(xml_arc.tag)
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = float(xml_arc.attrib.get("order") or 1)
            arc_qname = self._make_qname(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        if not isinstance(points_to, IReportElement) and not isinstance(points_to, BrelReference):
            raise TypeError(
                f"When creating a reference network, points_to must be of type IReportElement or BrelReference, not {type(points_to)}"
            )

        return ReferenceNetworkNode(points_to, [], arc_role, arc_qname, link_role, link_name, order)

    def update_report_elements(self, report_elements: Mapping[QName, IReportElement], network: INetwork):
        """
        Definition networks do not change the report elements
        :param report_elements: dict[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a DefinitionNetwork
        """
        pass

    def is_physical(self) -> bool:
        return True
