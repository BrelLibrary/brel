"""
This module contains the FootnoteNetworkNode class.
FootnoteNetworkNodes are used to represent nodes in a footnote network.
Since a node can have children, nodes can also be viewed as trees.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 30 January 2024

====================
"""

from typing import cast

from brel import Fact, QName
from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel.resource import BrelFootnote, IResource


class FootnoteNetworkNode(INetworkNode):
    """
    Class for representing a footnote network node in a footnote network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    def __init__(
        self,
        points_to: BrelFootnote | IReportElement | Fact,
        children: list["FootnoteNetworkNode"],
        arc_role: str,
        arc_name: QName,
        link_role: str,
        link_name: QName,
        order: float = 1.0,
    ) -> None:
        self.__points_to = points_to
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__order = order

    # First class citizens
    def get_report_element(self) -> IReportElement:
        if not isinstance(self.__points_to, IReportElement):
            raise ValueError(f"The FootnoteNetworkNode points to a resource. Use get_resource() instead")

        return self.__points_to

    def get_resource(self) -> IResource:
        if not isinstance(self.__points_to, IResource):
            raise ValueError(f"The FootnoteNetworkNode points to a report element. Use get_report_element() instead")
        return self.__points_to

    def get_fact(self) -> Fact:
        if not isinstance(self.__points_to, Fact):
            raise ValueError(f"The FootnoteNetworkNode points to a report element. Use get_report_element() instead")
        return self.__points_to

    def points_to(self) -> str:
        if isinstance(self.__points_to, IReportElement):
            return "report element"
        elif isinstance(self.__points_to, IResource):
            return "resource"
        elif isinstance(self.__points_to, Fact):
            return "fact"
        else:
            raise ValueError(f"The FootnoteNetworkNode points to an unknown type: {self.__points_to}")

    def get_children(self) -> list[INetworkNode]:
        return cast(list[INetworkNode], self.__children)

    def get_order(self) -> float:
        return self.__order

    def get_arc_role(self) -> str:
        return self.__arc_role

    def get_arc_name(self) -> QName:
        return self.__arc_name

    def get_link_role(self) -> str:
        return self.__link_role

    def get_link_name(self) -> QName:
        return self.__link_name

    # Internal methods
    def _add_child(self, child: INetworkNode):
        """
        Add a child to the node.
        :param child: the child to add
        """
        if not isinstance(child, FootnoteNetworkNode):
            raise ValueError(f"The child {child} is not a FootnoteNetworkNode")
        self.__children.append(child)
        self.__children.sort(key=lambda x: x.get_order())
