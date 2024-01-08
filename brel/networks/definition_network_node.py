"""
This module contains the DefinitionNetworkNode class.
DefinitionNetworkNodes are used to represent nodes in a definition network.
Since a node can have children, nodes can also be viewed as trees.
Note: the balance consistency check is not implemented here, but in the DefinitionNetwork class.

@author: Robin Schmidiger
@version: 0.5
@date: 04 January 2024
"""

from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel import Fact, QName

from typing import cast

from brel.resource import IResource


class DefinitionNetworkNode(INetworkNode):
    """
    Class for representing a definition network node in a definition network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    def __init__(
        self,
        report_element: IReportElement,
        children: list["DefinitionNetworkNode"],
        arc_role: str,
        arc_name: QName,
        link_role: str,
        link_name: QName,
        order: float = 1,
    ) -> None:
        self.__report_element = report_element
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__order = order

    # First class citizens
    def get_report_element(self) -> IReportElement:
        return self.__report_element

    def get_resource(self) -> IResource:
        raise ValueError("DefinitionNetworkNode does not point to a resource")

    def get_fact(self) -> Fact:
        raise ValueError("DefinitionNetworkNode does not point to a fact")

    def points_to(self) -> str:
        return "report element"

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
        if not isinstance(child, DefinitionNetworkNode):
            raise ValueError("Child must be of type DefinitionNetworkNode")

        self.__children.append(child)
        self.__children.sort(key=lambda node: node.get_order())

    def _set_report_element(self, report_element: IReportElement):
        """
        Set the report element of this node
        @param report_element: IReportElement to be set as the report element
        """
        self.__report_element = report_element
