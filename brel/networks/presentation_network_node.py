"""
This module contains the PresentationNetworkNode class.
PresentationNetworkNodes are used to represent nodes in a presentation network.
Since a node can have children, nodes can also be viewed as trees.

====================

- author: Robin Schmidiger
- version: 0.11
- date: 30 January 2024

====================
"""

from typing import cast, Callable

from brel import Fact, QName
from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel.resource import IResource


class PresentationNetworkNode(INetworkNode):
    """
    Class for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    def __init__(
        self,
        report_element: IReportElement,
        children: list["PresentationNetworkNode"],
        arc_role: str,
        arc_name: QName,
        link_role: str,
        link_name: QName,
        preferred_label_role: str | None,
        order: float = 1,
    ):
        self.__report_element = report_element
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__preferred_label_role = preferred_label_role
        self.__order = order

        # check if there is a label that matches the preferred label role
        # if not, raise an error

        if preferred_label_role is not None and not report_element.has_label_with_role(preferred_label_role):
            raise ValueError(f"report element {report_element} does not have a label with role {preferred_label_role}")

    # First class citizens
    def get_report_element(self) -> IReportElement:
        """
        :return: IReportElement associated with this node
        """
        return self.__report_element

    def get_resource(self) -> IResource:
        """
        Presentation network nodes do not point to resources, only to report elements.
        :raises ValueError: if this node does not point to a resource.
        Use the points_to method to check if this node points to a resource.
        """
        raise ValueError("PresentationNetworkNode does not point to a resource")

    def get_fact(self) -> Fact:
        """
        Presentation network nodes do not point to facts, only to report elements.
        :raises ValueError: if this node does not point to a fact.
        Use the points_to method to check if this node points to a fact.
        """
        raise ValueError("PresentationNetworkNode does not point to a fact")

    def points_to(self) -> str:
        """
        :return: str containing 'report element'
        """
        return "report element"

    def get_children(self) -> list["INetworkNode"]:
        """
        :returns list[NetworkNode]: containing the children of this node
        """
        # return lsitself.__children

        return cast(list["INetworkNode"], self.__children)

    def get_preferred_label_role(self) -> str | None:
        """
        Returns the preferred label role of this node
        :returns str: containing the preferred label role of this node
        """
        return self.__preferred_label_role

    def get_order(self) -> float:
        """
        Returns the order of this node
        :returns int: containing the order of this node
        """
        return self.__order

    def get_link_role(self) -> str:
        return self.__link_role

    def get_link_name(self) -> QName:
        return self.__link_name

    # Second class citizens
    def get_arc_role(self) -> str:
        return self.__arc_role

    def get_arc_name(self) -> QName:
        return self.__arc_name

    def __str__(self) -> str:
        """
        :return str: A string reporesentation of this node
        """

        return f"NetworkNode(report_element={self.__report_element}, no. children={len(self.__children)}"

    # Internal methods
    def _add_child(self, child: INetworkNode):
        """
        Add a child to this node
        :param child: The child node to be added
        :raises TypeError: if child is not of type PresentationNetworkNode
        """
        if not isinstance(child, PresentationNetworkNode):
            raise TypeError("child must be of type PresentationNetworkNode")

        self.__children.append(child)
        self.__children.sort(key=lambda node: node.get_order())
