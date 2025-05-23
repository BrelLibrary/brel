"""
This file contains the XMLLabelNetworkFactory class
XMLLabelNetworkFactories are used to create physical LabelNetworks from XML.
This module is usedc by the XML network parser to build physical label networks.

====================

- author: Robin Schmidiger
- version: 0.8
- date: 9 May 2025

====================
"""

from typing import cast

from lxml.etree import _Element  # type: ignore

from brel.brel_fact import Fact
from brel.networks import (
    INetwork,
    INetworkNode,
    LabelNetwork,
    LabelNetworkNode,
)
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import (
    qname_from_str,
    to_namespace_localname_notation,
)
from brel.reportelements import IReportElement
from brel.resource import BrelLabel, IResource
from brel.data.report_element.report_element_repository import ReportElementRepository


class LabelNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link: _Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role")
        )
        link_qname = qname_from_str(xml_link.tag, xml_link)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, LabelNetworkNode) for root in roots):
            raise TypeError("roots must all be of type LabelNetworkNode")

        roots_cast = cast(list[LabelNetworkNode], roots)

        return LabelNetwork(roots_cast, link_role, link_qname, self.is_physical())

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
            arc_qname = qname_from_str("link:unknown", xml_link)
        elif get_str_attribute(xml_arc, "xlink:from") == label:
            # the node is a root
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif get_str_attribute(xml_arc, "xlink:to", None) == label:
            # the node is an inner node
            arc_role = get_str_attribute(xml_arc, "xlink:arcrole")
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(xml_link, "xlink:role")
        link_name = qname_from_str(xml_link.tag, xml_link)

        if not isinstance(points_to, BrelLabel) and not isinstance(
            points_to, IReportElement
        ):
            raise TypeError(
                f"'points_to' must be of type BrelLabel or IReportElement, not {type(points_to)}"
            )

        return LabelNetworkNode(points_to, arc_role, arc_qname, link_role, link_name)

    def update_report_elements(
        self, report_element_repository: ReportElementRepository, network: INetwork
    ):
        """
        Label networks add the labels to the report elements
        :param report_elements: dict[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a CalculationNetwork
        :returns dict[QName, IReportElement]: containing all report elements. same as the report_elements parameter
        """

        # label networks tend to be nearly flat. The roots are the report element nodes and their children are label nodes
        for root in network.get_roots():
            if not isinstance(root, LabelNetworkNode):
                raise TypeError("roots must all be of type LabelNetworkNode")
            if not root.points_to() == "report element":
                raise ValueError(f"root {root} is not a report element")

            report_element = root.get_report_element()
            for label_node in root.get_children():
                if not isinstance(label_node, LabelNetworkNode):
                    raise TypeError("children must all be of type LabelNetworkNode")
                if not label_node.points_to() == "resource":
                    raise ValueError(f"child {label_node} is not a resource")

                label = label_node.get_resource()

                report_element._add_label(label)  # type: ignore

    def is_physical(self) -> bool:
        return True
