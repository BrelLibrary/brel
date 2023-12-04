import lxml.etree

from brel import QName
from brel.networks import INetwork, INetworkNode, PresentationNetworkNode
from brel.reportelements import *

from typing import cast

class PresentationNetwork(INetwork):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a Component.
    """
    # TODO: write docstrings
    def __init__(self, root: PresentationNetworkNode, link_role: str, link_name: QName) -> None:
        roots_copy = [cast(INetworkNode, root)]
        super().__init__(roots_copy, link_role, link_name, True)
    