"""
Contains the class for representing a label network node in a label network.
Label networks are what associates labels with report elements.
A label network node are references to either the report elements or the labels in the label linkbase.

====================

- author: Robin Schmidiger
- version: 0.8
- date: 30 January 2024

====================
"""

from typing import cast
from brel import Fact, QName
from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel.resource import BrelLabel

DEBUG = False


class LabelNetworkNode(INetworkNode):
    """
    Class for representing a label network node in a label network.
    Label networks are essentially sets of individual report elements.
    """

    def __init__(
        self,
        points_to: IReportElement | BrelLabel,
        arc_role: str,
        arc_name: QName,
        link_role: str,
        link_name: QName,
    ) -> None:
        self.__points_to = points_to
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__children: list[INetworkNode] = []

    # First class citizens
    def get_report_element(self) -> IReportElement:
        if not isinstance(self.__points_to, IReportElement):
            raise ValueError("LabelNetworkNodes do not point to report elements")

        return self.__points_to

    def get_resource(self) -> BrelLabel:
        if not isinstance(self.__points_to, BrelLabel):
            raise ValueError("LabelNetworkNodes do not point to resources")
        return self.__points_to

    def get_fact(self) -> Fact:
        raise ValueError("LabelNetworkNodes do not point to facts")

    def points_to(self) -> str:
        if isinstance(self.__points_to, IReportElement):
            return "report element"
        elif isinstance(self.__points_to, BrelLabel):
            return "resource"
        else:
            raise ValueError("LabelNetworkNodes do not point to report elements or resources")

    def get_children(self) -> list[INetworkNode]:
        return self.__children

    def get_order(self) -> int:
        return 1

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
        Adds a child to this node.
        :param child: INetworkNode to be added as a child
        """
        self.__children.append(child)
