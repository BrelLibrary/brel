from pybr import QName
from pybr.networks import INetwork, INetworkNode, LabelNetworkNode
from pybr.reportelements import *

from typing import cast

class LabelNetwork(INetwork):
    """
    Class for representing a label network.
    A label network is a network of nodes that represent the labels of a PyBRComponent.
    A label network is essentially a set of individual report elements. Unlike other networks,
    the label network is not associated with a component.
    """

    def __init__(self, roots: list[LabelNetworkNode], link_role: str, link_name: QName) -> None:
        self.__roots = roots
        self.__link_role = link_role
        self.__link_name = link_name
    
    # First class citizens
    def get_roots(self) -> list[INetworkNode]:
        """
        Get the root node of the presentation network
        @return: NetworkNode representing the root node of the network. Returns None if the network is empty.
        """
        return cast(list[INetworkNode], self.__roots)
    
    def get_link_role(self) -> str:
        """
        Get the link role of the presentation network
        @return: str containing the link role of the network. 
        Note: This returns the same as get_URL() on the PyBRComponent
        """
        return self.__link_role
    
    def get_link_name(self) -> QName:
        return self.__link_name
