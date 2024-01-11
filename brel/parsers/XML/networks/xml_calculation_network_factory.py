"""
This module contains the CalculationNetworkFactory class.
CalculationNetworkFactories are used to create CalculationNetworks from XML.
They are used by the XML parsers for networks to build calculation networks.

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
    CalculationNetwork,
    CalculationNetworkNode,
)
from brel.reportelements import IReportElement
from brel.resource import IResource
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils import get_str


class CalculationNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(
            xml_link_element.tag, self.get_qname_nsmap()
        )

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        if not all(isinstance(root, CalculationNetworkNode) for root in roots):
            raise TypeError("roots must all be of type CalculationNetworkNode")

        if link_role is None:
            raise ValueError("link_role must not be None")

        roots_cast = cast(list[CalculationNetworkNode], roots)

        return CalculationNetwork(roots_cast, link_role, link_qname)

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
            weight = 0.0
            arc_role = "unknown"
            order: float = 1
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            weight = 0.0
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = 1
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            weight = float(xml_arc.attrib.get("weight") or 0.0)
            arc_role = get_str(xml_arc, "{" + nsmap["xlink"] + "}arcrole")
            order = float(get_str(xml_arc, "order", "1.0"))
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        link_role = get_str(xml_link, "{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        # also, all calculation network nodes have to point to a concept
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type Concept, not {type(points_to)}"
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

    def update_report_elements(
        self, report_elements: dict[QName, IReportElement], _: INetwork
    ) -> dict[QName, IReportElement]:
        """
        Calculation networks do not change the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a CalculationNetwork
        @return: dict[QName, IReportElement] containing all report elements. same as the report_elements parameter
        """
        return report_elements

    def is_physical(self) -> bool:
        return True
