from brel import QName
from brel.networks import INetwork, INetworkNode, LabelNetworkNode
from brel.reportelements import *

from typing import cast


class LabelNetwork(INetwork):
    """
    Class for representing a label network.
    A label network is a network of nodes that represent the labels of a Component.
    A label network is essentially a set of individual report elements. Unlike other networks,
    the label network is not associated with a component.
    """

    def __init__(
        self, roots: list[LabelNetworkNode], link_role: str, link_name: QName
    ) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, True)
