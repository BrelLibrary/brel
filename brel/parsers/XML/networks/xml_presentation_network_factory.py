"""
This module contains the XMLPresentationNetworkFactory class.
XMLPresentationNetworkFactories are used to create PresentationNetworks from XML.
This module is used by the XML network parser to build presentation networks.

====================

- author: Robin Schmidiger
- version: 0.8
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
    PresentationNetwork,
    PresentationNetworkNode,
)
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import qname_from_str, to_namespace_localname_notation
from brel.reportelements import IReportElement
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.resource import BrelLabel, IResource


class PresentationNetworkFactory(IXMLNetworkFactory):
    def create_network(
        self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        """
        Create a PresentationNetwork from an XML link element and a list of roots.
        :param xml_link_element: lxml.etree._Element containing the link element
        :param roots: list[INetworkNode] containing the roots of the network
        :returns PresentationNetwork: The PresentationNetwork
        """
        if not all(isinstance(root, PresentationNetworkNode) for root in roots):
            raise TypeError("roots must be of type PresentationNetworkNode")

        roots_cast = cast(list[PresentationNetworkNode], roots)

        link_role = get_str_attribute(
            xml_link_element, to_namespace_localname_notation("xlink", "role")
        )
        link_name = qname_from_str(xml_link_element.tag, xml_link_element)

        return PresentationNetwork(roots_cast, link_role, link_name, self.is_physical())

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        """
        Create a PresentationNetworkNode from an XML link, an XML referenced element, an XML arc, and a points_to object.
        :param xml_link: lxml.etree._Element containing the link element
        :param xml_referenced_element: lxml.etree._Element containing the referenced element
        :param xml_arc: lxml.etree._Element containing the arc element
        :param points_to: IReportElement | IResource | Fact containing the object that the node points to
        :returns PresentationNetworkNode: The PresentationNetworkNode
        """

        label = get_str_attribute(
            xml_referenced_element, to_namespace_localname_notation("xlink", "label")
        )

        if xml_arc is None:
            # the node is not connected to any other node
            preferred_label_role = None
            arc_role = "unknown"
            order: float = 1
            arc_qname = qname_from_str("link:unknown", xml_referenced_element)
        elif (
            get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "from"), None
            )
            == label
        ):
            # the node is a root
            preferred_label_role = None
            arc_role = get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "arcrole")
            )
            order = 1
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        elif (
            get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "to"), None
            )
            == label
        ):
            # the node is an inner node
            preferred_label = get_str_attribute(
                xml_arc, "preferredLabel", BrelLabel.STANDARD_LABEL_ROLE
            )

            preferred_label_role = preferred_label
            arc_role = get_str_attribute(
                xml_arc, to_namespace_localname_notation("xlink", "arcrole")
            )
            order = float(get_str_attribute(xml_arc, "order", "1"))
            arc_qname = qname_from_str(xml_arc.tag, xml_arc)
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = get_str_attribute(
            xml_link, to_namespace_localname_notation("xlink", "role")
        )
        link_name = qname_from_str(xml_link.tag, xml_link)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        return PresentationNetworkNode(
            points_to,
            [],
            arc_role,
            arc_qname,
            link_role,
            link_name,
            preferred_label_role,
            order,
        )

    def is_physical(self) -> bool:
        return False
