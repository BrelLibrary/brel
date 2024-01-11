"""
Networks in XBRL are used to define relationships between different things in a filing.
For example

- Presentation networks define a hierarchy of report elements
- Calculation networks define which concepts should be the sum of which other concepts
- Definition networks define what the relationship between the types of the report elements are
- Label networks establish relationships between report elements and human readable labels
- Reference networks establish a link between report elements and other resources such as websites or documents

All networks in brel are represented by the INetwork interface.

Since only the calculation network has any special functionality thus far, the other networks are not part of this documentation.
They are all implemented in the same way as the calculation network and can be inspected using their shared interface INetwork.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 07 January 2024

====================
"""

from brel import QName
from brel.reportelements import *
from brel.networks import INetworkNode

from abc import ABC, abstractmethod


class INetwork(ABC):
    """
    Interface for representing networks in Brel.
    The networks are defined according to the XBRL Generic Links 1.0 specification
    available [HERE](https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html)
    """

    def __init__(
        self,
        roots: list[INetworkNode],
        link_role: str,
        link_name: QName,
        is_physical: bool,
    ) -> None:
        self.__roots = roots
        self.__link_role = link_role
        self.__link_name = link_name
        self.__is_physical = is_physical

    # First class citizens
    def get_roots(self) -> list[INetworkNode]:
        """
        Get all root nodes of the network
        :returns list[NetworkNode]: representing the root nodes of the network.
        """
        return self.__roots

    def get_link_role(self) -> str:
        """
        Get the link role of the network
        :returns str: containing the link role of the network.
        Note: This returns the same as `get_URL()` on the parent component
        """
        return self.__link_role

    def get_link_name(self) -> QName:
        """
        Get the link name of the network
        :returns QName: link name of the network. e.g. for presentation networks this is usually "link:presentationLink"
        """
        return self.__link_name

    def is_physical(self) -> bool:
        """
        Check if the network is a physical network
        Physical networks must have the same link/arc role/name across all nodes
        :returns bool: indicating if the network is a physical network
        """
        return self.__is_physical

    # Second class citizens
    def get_arc_roles(self) -> list[str]:
        """
        Get all the arc roles that are used by nodes in the network
        :returns list[str]: list of all arc roles that are used by nodes in the network
        """
        arc_role_set = set(
            [node.get_arc_role() for node in self.get_all_nodes()]
        )
        return list(arc_role_set)

    def get_arc_name(self) -> QName | None:
        """
        Get the arc name of all the arcs in the network. All arcs in the network have the same arc name.
        :returns QName|None: The arc name of all the arcs in the network. Returns None if the network is empty.
        """
        roots = self.get_roots()
        if len(roots) == 0:
            return None
        else:
            return roots[0].get_arc_name()

    def get_root(self) -> INetworkNode:
        """
        Get the root node of the network if the network has only one root.
        Note that each network must have at least one root node.
        :returns NetworkNode: representing the root node of the network.
        :raises ValueError: if the network has multiple roots
        """
        roots = self.get_roots()
        if len(roots) > 1:
            raise ValueError(
                f"Cannot call getRoot() for network with multiple roots"
            )
        return roots[0]

    def get_all_nodes(self) -> list[INetworkNode]:
        """
        Get all nodes in the network as a list
        :returns list[NetworkNode]: containing all nodes in the network
        """

        # create a set to store all nodes in
        nodes = set()

        # recursive function to add all children of a node to the nodes set
        def add_children(node: INetworkNode) -> None:
            nodes.add(node)
            for child in node.get_children():
                add_children(child)

        # add all children of the root node to the nodes set
        roots: list[INetworkNode] = self.get_roots()
        for root in roots:
            add_children(root)

        # return the nodes set as a list
        return list(nodes)
