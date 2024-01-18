"""
This module contains the interface for a node in a network.
All nodes in a network are built on a common interface that allows for some basic navigation of the network.
The network node interface also contains some utility methods for working with networks and nodes.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 2023-12-29

====================
"""

from abc import ABC, abstractmethod

from brel import Fact, QName
from brel.reportelements import IReportElement
from brel.resource import IResource


class INetworkNode(ABC):
    """
    Interface for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.

    Each node in a network can point to one of the following:

    - A report element [IReportElement](#./reportelements/i_report_element.md): use `node.get_report_element()`
    - A resource[IResource](#./resource/i_resource.md): use `node.get_resource()`
    - A fact[Fact](#./facts/fact.md):

    The getter methods above will raise a ValueError if the node does not point to the requested type.
    Use the `points_to()` method to check if the node points to a report element, resource or fact.

    - If the node points to a report element, `points_to()` will return 'report element'
    - If the node points to a resource, `points_to()` will return 'resource'
    - If the node points to a fact, `points_to()` will return 'fact'

    To navigate the network, use the `get_children()` method to get the children of a node.

    Each node also has an order attribute which can be accessed using the `get_order()` method.
    The children of a node are ordered by their order attribute.

    """

    # First class citizens
    @abstractmethod
    def get_report_element(self) -> IReportElement:
        """
        :returns IReportElement: report element associated with this node.
        :raises ValueError: if this node does not point to a report element.
        Use the `points_to()` method to check if this node points to a report element.
        """
        raise NotImplementedError

    @abstractmethod
    def get_resource(self) -> IResource:
        """
        :returns IResource: resource associated with this node.
        :raises ValueError: if this node does not point to a resource.
        Use the `points_to()` method to check if this node points to a resource.
        """
        raise NotImplementedError

    @abstractmethod
    def get_fact(self) -> Fact:
        """
        :returns Fact: fact associated with this node.
        :raises ValueError: if this node does not point to a fact.
        Use the `points_to()` method to check if this node points to a fact.
        """
        raise NotImplementedError

    @abstractmethod
    def points_to(self) -> str:
        """
        Returns
        - 'resource' if this node points to a resource
        - 'report element' if this node points to a report element
        - 'fact' if this node points to a fact
        :returns str: containing 'resource', 'report element' or 'fact'
        """
        raise NotImplementedError

    @abstractmethod
    def get_children(self) -> list["INetworkNode"]:
        """
        Returns all children of this node
        :returns list[NetworkNode]: list containing the children of this node
        """
        raise NotImplementedError

    @abstractmethod
    def get_arc_role(self) -> str:
        """
        :returns str: the arc role of this node. There can be nodes with different arc roles in the same network.
        """
        raise NotImplementedError

    @abstractmethod
    def get_arc_name(self) -> QName:
        """
        :returns QName: the arc name of this node. All nodes in the same network have the same arc name.
        """
        raise NotImplementedError

    @abstractmethod
    def get_link_role(self) -> str:
        """
        :returns str: the link role of this node. This is the same as the link role of the network that the node is in.
        """
        raise NotImplementedError

    @abstractmethod
    def get_link_name(self) -> QName:
        """
        :returns QName: the link name of this node. This is the same as the link name of the network that the node is in.
        """
        raise NotImplementedError

    # second class citizens
    def get_all_descendants(self) -> list["INetworkNode"]:
        """
        Returns all descendants of the current node
        :returns list[NetworkNode]: list containing all descendants of this node
        """
        descendants = set()
        worklist: list["INetworkNode"] = [self]
        while len(worklist) > 0:
            node = worklist.pop()
            descendants.add(node)
            worklist.extend(node.get_children())

        return list(descendants)

    def __str__(self) -> str:
        return f"NetworkNode(points_to={self.points_to()}, arc_role={self.get_arc_role()}, arc_name={self.get_arc_name()}, link_role={self.get_link_role()}, link_name={self.get_link_name()}, no. children={len(self.get_children())})"

    def is_leaf(self) -> bool:
        """
        :returns bool: True if this node is a leaf, False otherwise
        """
        return len(self.get_children()) == 0

    @abstractmethod
    def get_order(self) -> float:
        """
        :returns float: The order of this node. Nodes are ordered by their order attribute.
        """
        raise NotImplementedError

    # Internal methods
    def _add_child(self, child: "INetworkNode"):
        """
        Add a child to this node
        :param child: NetworkNode to be added as a child
        """
        raise NotImplementedError
