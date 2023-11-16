from pybr import QName
from pybr.reportelements import *
from pybr.networks import INetworkNode

from abc import ABC, abstractmethod

class INetwork(ABC):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a PyBRComponent.
    """
    
    # First class citizens
    @abstractmethod
    def get_roots(self) -> list[INetworkNode]:
        """
        Get the root nodes of the presentation network
        @return: list[NetworkNode] representing the root nodes of the network.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_link_role(self) -> str:
        """
        Get the link role of the presentation network
        @return: str containing the link role of the network. 
        Note: This returns the same as get_URL() on the PyBRComponent
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_link_name(self) -> QName:
        """
        Get the link name of the network
        @return: QName containing the link name of the network. e.g. for presentation networks this is usually "link:presentationLink"
        """
        raise NotImplementedError

    # Second class citizens
    def get_root(self) -> INetworkNode:
        """
        Get the root node of the presentation network
        @return: NetworkNode representing the root node of the network.
        @raises ValueError: if the network has multiple roots
        """
        roots = self.get_roots()
        if len(roots) > 1:
            raise ValueError(f"Cannot call getRoot() for network with multiple roots")
        return roots[0]

    def get_all_nodes(self) -> list[INetworkNode]:
        """
        Get all nodes in the network
        @return: list[NetworkNode] containing all nodes in the network
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