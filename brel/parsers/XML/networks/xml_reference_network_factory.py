"""
This module contains the ReferenceNetworkFactory class.
ReferenceNetworkFactories are used to create ReferenceNetworks from XML.

@author: Robin Schmidiger
@version: 0.2
@date: 04 January 2024
"""

import lxml
import lxml.etree
from typing import cast
from brel import QName, QNameNSMap, Fact
from brel.networks import (
    INetwork,
    INetworkNode,
    ReferenceNetworkNode,
    ReferenceNetwork,
)
from brel.reportelements import *
from brel.resource import BrelReference, IResource

from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils import get_str


class ReferenceNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = get_str(xml_link, f"{{{nsmap['xlink']}}}role")
        link_qname = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if not all(isinstance(root, ReferenceNetworkNode) for root in roots):
            raise TypeError("roots must all be of type ReferenceNetworkNode")

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        roots_cast = cast(list[ReferenceNetworkNode], roots)

        return ReferenceNetwork(roots_cast, link_role, link_qname)

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = get_str(xml_referenced_element, f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(
                f"label attribute not found on referenced element {xml_referenced_element}"
            )

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 1.0
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            order = 1.0
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            order = float(xml_arc.attrib.get("order") or 1)
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str(xml_link, f"{{{nsmap['xlink']}}}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if not isinstance(points_to, IReportElement) and not isinstance(
            points_to, BrelReference
        ):
            raise TypeError(
                f"When creating a reference network, points_to must be of type IReportElement or BrelReference, not {type(points_to)}"
            )

        return ReferenceNetworkNode(
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
