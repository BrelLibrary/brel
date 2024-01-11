from brel import QName
from brel.networks import INetwork, INetworkNode, DefinitionNetworkNode
from brel.reportelements import *
from collections import defaultdict

from typing import cast


class DefinitionNetwork(INetwork):
    """
    Class for representing a definition network.
    A definition network is a network of nodes that represent the definition of a Component.
    """

    def __init__(
        self,
        roots: list[DefinitionNetworkNode],
        link_role: str,
        link_name: QName,
        is_physical: bool,
    ) -> None:
        roots_copy: list[INetworkNode] = [
            cast(INetworkNode, root) for root in roots
        ]
        super().__init__(roots_copy, link_role, link_name, is_physical)
