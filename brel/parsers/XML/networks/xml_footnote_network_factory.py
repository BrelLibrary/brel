"""
This module contains the XMLFootnoteNetworkFactory class.
XMLFootnoteNetworkFactories are used to create physical FootnoteNetworks from XML.
This module is used by the XML network parser to build physical footnote networks.
At the time of writing, footnote nodes are the only nodes that can point to facts.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 5 April 2025

====================
"""

from typing import cast, Mapping

import lxml
import lxml.etree

from brel.brel_fact import Fact
from brel.networks import (
    FootnoteNetwork,
    FootnoteNetworkNode,
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
from brel.reportelements import IReportElement
from brel.resource import BrelFootnote, IResource


class FootnoteNetworkFactory(IXMLNetworkFactory):
    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        link_role = get_str_attribute(xml_link, "xlink:role")
        link_qname = qname_from_str(xml_link.tag, xml_link)

        if not all(isinstance(root, FootnoteNetworkNode) for root in roots):
            raise TypeError("roots must all be of type FootnoteNetworkNode")

        if len(roots) == 0:
            raise ValueError("roots must not be empty")

        roots_cast = cast(list[FootnoteNetworkNode], roots)

        return FootnoteNetwork(roots_cast, link_role, link_qname, self.is_physical())

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
            arc_role: str = "unknown"
            order = 1.0
            arc_qname = qname_from_str("link:unknown", xml_referenced_element)
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
            arc_qname = qname_from_str("link:unknown", xml_referenced_element)
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

        if isinstance(points_to, IResource) and not isinstance(points_to, BrelFootnote):
            raise ValueError(
                f"points_to must be of type BreelFootnote, not {type(points_to)}"
            )

        return FootnoteNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, order
        )

    def is_physical(self) -> bool:
        return True
