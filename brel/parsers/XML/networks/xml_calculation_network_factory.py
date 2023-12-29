import lxml
import lxml.etree
from typing import cast
from brel import QName, QNameNSMap
from brel.networks import (
    INetwork,
    INetworkNode,
    CalculationNetwork,
    CalculationNetworkNode,
)
from brel.reportelements import IReportElement
from brel.resource import IResource
from brel.parsers.XML.networks import IXMLNetworkFactory


class CalculationNetworkFactory(IXMLNetworkFactory):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        super().__init__(qname_nsmap)

    def create_network(
        self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
        nsmap = self.get_qname_nsmap().get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link_element.tag, self.get_qname_nsmap())

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
        points_to: IReportElement | IResource,
    ) -> INetworkNode:
        nsmap = self.get_qname_nsmap().get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(
                f"label attribute not found on referenced element {xml_referenced_element}"
            )

        if xml_arc is None:
            # the node is not connected to any other node
            weight = 0.0
            arc_role = "unknown"
            order = 1
            arc_qname = QName.from_string("link:unknown", self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            weight = 0.0
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = 1
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            weight = float(xml_arc.attrib.get("weight") or 0.0)
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            order = float(xml_arc.attrib.get("order") or 1.0)
            arc_qname = QName.from_string(xml_arc.tag, self.get_qname_nsmap())
        else:
            raise ValueError(
                f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}"
            )

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag, self.get_qname_nsmap())

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(
                f"arcrole attribute on arc element {xml_arc} is not a string"
            )

        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(
                f"role attribute on link element {xml_link} is not a string"
            )

        # check if 'points_to' is a ReportElement
        if not isinstance(points_to, IReportElement):
            raise TypeError(
                f"points_to must be of type IReportElement, not {type(points_to)}"
            )

        # also, all calculation network nodes have to point to a concept
        if not isinstance(points_to, IReportElement):
            raise TypeError(f"points_to must be of type Concept, not {type(points_to)}")

        return CalculationNetworkNode(
            points_to, [], arc_role, arc_qname, link_role, link_name, weight, order
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
