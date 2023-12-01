from pybr import QName
from pybr.networks import INetwork, INetworkNode, ReferenceNetworkNode
from pybr.reportelements import *

from typing import cast

class ReferenceNetwork(INetwork):
    """
    Class for representing a Reference network.
    A Reference network is a network of nodes that represent the Reference of a PyBRComponent.
    """

    def __init__(self, roots: list[ReferenceNetworkNode], link_role: str, link_name: QName) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, True)