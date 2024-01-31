from typing import cast

from brel import QName
from brel.networks import FootnoteNetworkNode, INetwork, INetworkNode
from brel.reportelements import *


class FootnoteNetwork(INetwork):
    """
    Class for representing a footnote network.
    A footnote network contains nodes that represent footnotes.
    """

    def __init__(
        self,
        roots: list[FootnoteNetworkNode],
        link_role: str,
        link_name: QName,
        is_physical: bool,
    ) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, is_physical)
