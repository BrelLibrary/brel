"""
This file contains the XMLLabelNetworkFactory class
XMLLabelNetworkFactories are used to create physical LabelNetworks from XML.
This module is usedc by the XML network parser to build physical label networks.

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
    LabelNetwork,
    LabelNetworkNode,
)
from brel.reportelements import IReportElement
from brel.resource import BrelLabel, IResource

from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils import get_str


class LabelNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = get_str(xml_link_element, f"{{{nsmap['xlink']}}}role")
        link_qname = QName.from_string(
            xml_link_element.tag, self.get_qname_nsmap()
        )

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, LabelNetworkNode) for root in roots):
            raise TypeError("roots must all be of type LabelNetworkNode")

        roots_cast = cast(list[LabelNetworkNode], roots)

        return LabelNetwork(roots_cast, link_role, link_qname)

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
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str(xml_link, f"{{{nsmap['xlink']}}}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if not isinstance(points_to, BrelLabel) and not isinstance(
            points_to, IReportElement
        ):
            raise TypeError(
                f"'points_to' must be of type BrelLabel or IReportElement, not {type(points_to)}"
            )

        return LabelNetworkNode(
            points_to, arc_role, arc_qname, link_role, link_name
        )

    def update_report_elements(
        self,
        report_elements: dict[QName, IReportElement],
        label_network: INetwork,
    ) -> dict[QName, IReportElement]:
        """
        Label networks add the labels to the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a CalculationNetwork
        @return: dict[QName, IReportElement] containing all report elements. same as the report_elements parameter
        """

        # label networks tend to be nearly flat. The roots are the report element nodes and their children are label nodes
        for root in label_network.get_roots():
            if not isinstance(root, LabelNetworkNode):
                raise TypeError("roots must all be of type LabelNetworkNode")
            if not root.points_to() == "report element":
                raise ValueError(f"root {root} is not a report element")

            report_element = root.get_report_element()
            for label_node in root.get_children():
                if not isinstance(label_node, LabelNetworkNode):
                    raise TypeError(
                        "children must all be of type LabelNetworkNode"
                    )
                if not label_node.points_to() == "resource":
                    raise ValueError(f"child {label_node} is not a resource")

                label = label_node.get_resource()
                if not isinstance(label, BrelLabel):
                    raise TypeError(
                        f"label {label} is not a BrelLabel. It is of type {type(label)}"
                    )

                report_element._add_label(label)

        return report_elements

    def is_physical(self) -> bool:
        return True
