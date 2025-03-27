"""
This file contains the XMLLabelNetworkFactory class
XMLLabelNetworkFactories are used to create physical LabelNetworks from XML.
This module is usedc by the XML network parser to build physical label networks.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 30 January 2024

====================
"""

from typing import cast, Mapping

import lxml
import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import (
    INetwork,
    INetworkNode,
    LabelNetwork,
    LabelNetworkNode,
)
from brel.parsers.utils import get_str
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.reportelements import IReportElement
from brel.resource import BrelLabel, IResource


class LabelNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        link_role = get_str(xml_link_element, self._clark("xlink", "role"))
        link_qname = self._make_qname(xml_link_element.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, LabelNetworkNode) for root in roots):
            raise TypeError("roots must all be of type LabelNetworkNode")

        roots_cast = cast(list[LabelNetworkNode], roots)

        return LabelNetwork(roots_cast, link_role, link_qname, self.is_physical())

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
            arc_qname = self._make_qname("link:unknown")
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            # the node is a root
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            arc_qname = self._make_qname(xml_arc.tag)
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            # the node is an inner node
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            arc_qname = self._make_qname(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        if not isinstance(points_to, BrelLabel) and not isinstance(points_to, IReportElement):
            raise TypeError(f"'points_to' must be of type BrelLabel or IReportElement, not {type(points_to)}")

        return LabelNetworkNode(points_to, arc_role, arc_qname, link_role, link_name)

    def update_report_elements(
        self,
        _: Mapping[QName, IReportElement],
        label_network: INetwork,
    ):
        """
        Label networks add the labels to the report elements
        :param report_elements: dict[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a CalculationNetwork
        :returns dict[QName, IReportElement]: containing all report elements. same as the report_elements parameter
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
                    raise TypeError("children must all be of type LabelNetworkNode")
                if not label_node.points_to() == "resource":
                    raise ValueError(f"child {label_node} is not a resource")

                label = label_node.get_resource()
                if not isinstance(label, BrelLabel):
                    raise TypeError(f"label {label} is not a BrelLabel. It is of type {type(label)}")

                report_element._add_label(label)

    def is_physical(self) -> bool:
        return True
