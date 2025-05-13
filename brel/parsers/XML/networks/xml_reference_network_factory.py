"""
This module contains the ReferenceNetworkFactory class.
ReferenceNetworkFactories are used to create ReferenceNetworks from XML.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 5 April 2025

====================
"""

from typing import cast

import lxml
import lxml.etree

from brel.brel_fact import Fact
from brel.networks import (
    INetwork,
    INetworkNode,
    ReferenceNetwork,
    ReferenceNetworkNode,
)
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import qname_from_str, to_namespace_localname_notation
from brel.reportelements import *
from brel.resource import BrelReference, IResource


class ReferenceNetworkFactory(IXMLNetworkFactory):
    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role")
        )
        link_qname = qname_from_str(xml_link.tag, xml_link)

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
        label = get_str_attribute(
            xml_referenced_element, to_namespace_localname_notation("xlink", "label")
        )

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            order = 1.0
            arc_qname = qname_from_str("link:unknown", xml_link)
        elif (
            get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "from"), None
            )
            == label
        ):
            # the node is a root
            arc_role = get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "arcrole")
            )
            order = 1.0
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif (
            get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "to"), None
            )
            == label
        ):
            # the node is an inner node
            arc_role = get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "arcrole")
            )
            order = float(xml_arc.attrib.get("order") or 1)
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role")
        )
        link_name = qname_from_str(xml_link.tag, xml_link)

        if not isinstance(points_to, IReportElement) and not isinstance(
            points_to, BrelReference
        ):
            raise TypeError(
                f"When creating a reference network, points_to must be of type IReportElement or BrelReference, not {type(points_to)}"
            )

        return ReferenceNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def is_physical(self) -> bool:
        return True
