"""
This module contains the PresentationNetwork class.
"""

from typing import cast

from brel import QName
from brel.networks import INetwork, INetworkNode, PresentationNetworkNode
from brel.reportelements import *


class PresentationNetwork(INetwork):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a Component.
    """

    def __init__(
        self, root: PresentationNetworkNode, link_role: str, link_name: QName
    ) -> None:
        roots_copy = [cast(INetworkNode, root)]
        super().__init__(roots_copy, link_role, link_name, True)
