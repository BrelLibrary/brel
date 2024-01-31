"""
Contains the ReferenceNetwork class, which acts as a wrapper for reference network nodes.

====================

- author: Robin Schmidiger
- version: 0.1
- date: 04 January 2024

====================
"""

from typing import cast

from brel import QName
from brel.networks import INetwork, INetworkNode, ReferenceNetworkNode
from brel.reportelements import *


class ReferenceNetwork(INetwork):
    """
    Class for representing a Reference network.
    A Reference network is a network of nodes that represent the Reference of a Component.
    """

    def __init__(
        self,
        roots: list[ReferenceNetworkNode],
        link_role: str,
        link_name: QName,
        is_physical: bool,
    ) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, is_physical)
