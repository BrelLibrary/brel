"""
This module contains the XMLPresentationNetworkFactory class.
XMLPresentationNetworkFactories are used to create PresentationNetworks from XML.
This module is usedc by the XML network parser to build presentation networks.

@author: Robin Schmidiger
@version: 0.4
@date: 04 January 2024
"""

import lxml
import lxml.etree
from typing import cast
from brel import QName, BrelLabelRole, QNameNSMap, Fact
from brel.reportelements import IReportElement, Abstract, Hypercube, LineItems
from brel.networks import (
    INetwork,
    INetworkNode,
    PresentationNetwork,
    PresentationNetworkNode,
)
from brel.resource import IResource
from brel.parsers.XML.networks import IXMLNetworkFactory
from brel.parsers.utils import get_str


class PresentationNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        # TODO: turn this into a get_url)from_prefix and make_qname methods
        nsmap = self.get_qname_nsmap().get_nsmap()

        if len(roots) != 1:
            root_report_element_names = list(
                map(lambda x: str(x.get_report_element().get_name()), roots)
            )
            raise ValueError(
                f"roots must have length 1, not {len(roots)}. The network has the roots {root_report_element_names}"
            )
        if not isinstance(roots[0], PresentationNetworkNode):
            raise TypeError("roots must be of type PresentationNetworkNode")

        root = roots[0]
        link_role = get_str(xml_link_element, f"{{{nsmap['xlink']}}}role")
        link_name = QName.from_string(
            xml_link_element.tag, self.get_qname_nsmap()
        )

        if link_role is None:
            raise ValueError("link_role must not be None")

        return PresentationNetwork(root, link_role, link_name)

    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        # label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        label = get_str(xml_referenced_element, f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(
                f"label attribute not found on referenced element {xml_referenced_element}"
            )

        if xml_arc is None:
            # the node is not connected to any other node
            preferred_label_role = None
            arc_role = "unknown"
            order: float = 1
            arc_qname = QName.from_string(
                "link:unknown", self.get_qname_nsmap()
            )
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            preferred_label_role = None
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            order = 1
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            # preferred_label = xml_arc.attrib.get("preferredLabel")
            preferred_label = get_str(
                xml_arc, "preferredLabel", BrelLabelRole.STANDARD_LABEL.value
            )
            if (
                not isinstance(preferred_label, str)
                and preferred_label is not None
            ):
                raise TypeError(
                    f"preferredLabel attribute on arc element {xml_arc} is not a string. It is {type(preferred_label)}"
                )

            if preferred_label is None:
                preferred_label_role = None
            else:
                preferred_label_role = BrelLabelRole.from_url(preferred_label)
            # arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            arc_role = get_str(xml_arc, f"{{{nsmap['xlink']}}}arcrole")
            # order = float(xml_arc.attrib.get("order") or 1)
            order = float(get_str(xml_arc, "order", "1"))
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if arc_role is None:
            raise ValueError(
                f"arcrole attribute not found on arc element {xml_arc}"
            )
        if not isinstance(arc_role, str):
            raise TypeError(
                f"arcrole attribute on arc element {xml_arc} is not a string"
            )
        if link_role is None:
            raise ValueError(
                f"role attribute not found on link element {xml_link}"
            )
        if not isinstance(link_role, str):
            raise TypeError(
                f"role attribute on link element {xml_link} is not a string"
            )

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

    def update_report_elements(
        self, report_elements: dict[QName, IReportElement], network: INetwork
    ) -> dict[QName, IReportElement]:
        """
        Promote abstracts to line items
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a PresentationNetwork
        @return: dict[QName, IReportElement] containing all report elements, some of which may have been promoted to line items.
        """
        if not isinstance(network, PresentationNetwork):
            raise TypeError("network must be of type PresentationNetwork")

        # find the nodes to promote
        nodes_to_promote: list[PresentationNetworkNode] = []
        nodes = cast(list[PresentationNetworkNode], network.get_all_nodes())
        for node in nodes:
            if isinstance(node.get_report_element(), Abstract):
                parent = next(
                    filter(lambda x: node in x.get_children(), nodes), None
                )

                # promote if the node is abstract and the parent is a hypercube
                if parent is not None and isinstance(
                    parent.get_report_element(), Hypercube
                ):
                    nodes_to_promote.append(node)

                hypercube_children = list(
                    filter(
                        lambda x: isinstance(
                            x.get_report_element(), Hypercube
                        ),
                        node.get_children(),
                    )
                )

                # promote if the node is abstract, it is the root and it has no hypercube children
                if parent is None and len(hypercube_children) == 0:
                    nodes_to_promote.append(node)

        # then promote the nodes
        for node in nodes_to_promote:
            abstract = cast(Abstract, node.get_report_element())
            line_items = LineItems(abstract.get_name(), abstract.get_labels())

            # update the report elements dict
            report_elements[line_items.get_name()] = line_items

            # update the node in the network
            node._set_report_element(line_items)

        return report_elements

    def is_physical(self) -> bool:
        return True
