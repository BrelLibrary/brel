"""
Contains the class ReferenceNetworkNode, which represents a reference network node in a reference network.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 30 January 2024

====================
"""

from typing import cast

from brel import Fact, QName
from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel.resource import BrelReference, IResource


class ReferenceNetworkNode(INetworkNode):
    """
    Class for representing a reference network node in a reference network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    def __init__(
        self,
        points_to: BrelReference | IReportElement,
        children: list["ReferenceNetworkNode"],
        arc_role: str,
        arc_name: QName,
        link_role: str,
        link_name: QName,
        order: float = 1,
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
            raise ValueError("ReferenceNetworkNodes do not point to report elements")

        return self.__points_to

    def get_resource(self) -> IResource:
        if not isinstance(self.__points_to, IResource):
            raise ValueError("ReferenceNetworkNodes do not point to resources")
        return self.__points_to

    def get_fact(self) -> Fact:
        raise ValueError("ReferenceNetworkNodes do not point to facts")

    def points_to(self) -> str:
        if isinstance(self.__points_to, IReportElement):
            return "report element"
        elif isinstance(self.__points_to, IResource):
            return "resource"
        else:
            raise ValueError("ReferenceNetworkNodes do not point to report elements or resources")

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
        if not isinstance(child, ReferenceNetworkNode):
            raise ValueError("Child must be of type ReferenceNetworkNode")

        self.__children.append(child)
        self.__children.sort(key=lambda node: node.get_order())
