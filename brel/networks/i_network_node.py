"""
Contains the interface for a node in a network.
Also contains some utility methods for working with networks and nodes.

@author: Robin Schmidiger
@version: 0.3
@date: 2023-12-29
"""

from abc import ABC, abstractmethod
from brel.reportelements import IReportElement
from brel import QName
from brel.resource import IResource


class INetworkNode(ABC):
    """
    Class for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    # First class citizens
    @abstractmethod
    def get_report_element(self) -> IReportElement:
        """
        Returns the report element associated with this node.
        @return: IReportElement associated with this node.
        @raises ValueError: if this node does not point to a report element.
        Use the points_to method to check if this node points to a report element.
        """
        raise NotImplementedError

    @abstractmethod
    def get_resource(self) -> IResource:
        """
        Returns the resource associated with this node.
        @return: IResource associated with this node.
        @raises ValueError: if this node does not point to a resource.
        Use the points_to method to check if this node points to a resource.
        """
        raise NotImplementedError

    @abstractmethod
    def is_a(self) -> str:
        """
        Returns
        - 'resource' if this node points to a resource
        - 'report element' if this node points to a report element
        @return: str containing 'resource' or 'report element'
        """
        raise NotImplementedError

    @abstractmethod
    def get_children(self) -> list["INetworkNode"]:
        """
        Returns the children of this node
        @return: list[NetworkNode] containing the children of this node
        """
        raise NotImplementedError

    @abstractmethod
    def get_arc_role(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_arc_name(self) -> QName:
        raise NotImplementedError

    @abstractmethod
    def get_link_role(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_link_name(self) -> QName:
        raise NotImplementedError

    # second class citizens
    def get_all_descendants(self) -> list["INetworkNode"]:
        """
        Returns a list containing all descendants of this node
        @return: list[NetworkNode] containing all descendants of this node
        """
        descendants = set()
        worklist = [self]
        while len(worklist) > 0:
            node = worklist.pop()
            descendants.add(node)
            worklist.extend(node.get_children())

        return list(descendants)

    def __str__(self) -> str:
        """
        Returns a string representation of this node
        @return: str containing a string representation of this node
        """

        return f"NetworkNode(report_element={self.get_report_element()}, no. children={len(self.get_children())}"

    def is_leaf(self) -> bool:
        """
        Returns true if this node is a leaf, false otherwise
        @return: bool containing true if this node is a leaf, false otherwise
        """
        return len(self.get_children()) == 0

    @abstractmethod
    def get_order(self) -> float:
        """
        Returns the order of this node in the network
        @return: int containing the order of this node in the network
        """
        raise NotImplementedError

    # Internal methods
    def add_child(self, child: "INetworkNode"):
        """
        Add a child to this node
        @param child: NetworkNode to be added as a child
        """
        raise NotImplementedError
