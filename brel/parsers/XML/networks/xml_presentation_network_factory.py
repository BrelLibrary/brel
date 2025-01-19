"""
This module contains the XMLPresentationNetworkFactory class.
XMLPresentationNetworkFactories are used to create PresentationNetworks from XML.
This module is used by the XML network parser to build presentation networks.

====================

- author: Robin Schmidiger
- version: 0.7
- date: 19 February 2024

====================
"""

from typing import cast, Mapping

import lxml
import lxml.etree

from brel import Fact, QName, QNameNSMap
from brel.networks import (
    INetwork,
    INetworkNode,
    PresentationNetwork,
    PresentationNetworkNode,
)
from brel.reportelements import IReportElement
from brel.parsers.utils import get_str, get_clark
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.resource import BrelLabel, IResource


class PresentationNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        """
        Create a PresentationNetwork from an XML link element and a list of roots.
        :param xml_link_element: lxml.etree._Element containing the link element
        :param roots: list[INetworkNode] containing the roots of the network
        :returns PresentationNetwork: The PresentationNetwork
        """
        if not all(isinstance(root, PresentationNetworkNode) for root in roots):
            raise TypeError("roots must be of type PresentationNetworkNode")

        roots_cast = cast(list[PresentationNetworkNode], roots)

        link_role = get_str(xml_link_element, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link_element.tag)

        if link_role is None:
            raise ValueError("link_role must not be None")

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

        label = get_str(xml_referenced_element, self._clark("xlink", "label"))

        if xml_arc is None:
            # the node is not connected to any other node
            preferred_label_role = None
            arc_role = "unknown"
            order: float = 1
            arc_qname = self._make_qname("link:unknown")
        elif get_str(xml_arc, self._clark("xlink", "from"), None) == label:
            # the node is a root
            preferred_label_role = None
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = 1
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif get_str(xml_arc, self._clark("xlink", "to"), None) == label:
            # the node is an inner node
            preferred_label = get_str(xml_arc, "preferredLabel", BrelLabel.STANDARD_LABEL_ROLE)

            if preferred_label is None:
                preferred_label_role = None
            else:
                preferred_label_role = preferred_label
            arc_role = get_str(xml_arc, self._clark("xlink", "arcrole"))
            order = float(get_str(xml_arc, "order", "1"))
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")

        link_role = get_str(xml_link, self._clark("xlink", "role"))
        link_name = self._make_qname(xml_link.tag)

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type IReportElement, not {type(points_to)}")

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

    def update_report_elements(self, report_elements: Mapping[QName, IReportElement], network: INetwork):
        """
        Promote abstracts to line items
        :param report_elements: dict[QName, IReportElement] containing all report elements
        :param network: INetwork containing the network. Must be a PresentationNetwork
        :return: dict[QName, IReportElement] containing all report elements, some of which may have been promoted to line items.
        """
        pass

    def is_physical(self) -> bool:
        return False
