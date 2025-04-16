"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 2 April 2025

====================
"""

from collections import defaultdict
from brel.data.network.network_repository import NetworkRepository
from brel.networks.i_network import INetwork


class InMemoryNetworkRepository(NetworkRepository):
    def __init__(self) -> None:
        self.__networks: dict[str, list[INetwork]] = defaultdict(list)

    def get(self, role: str) -> list[INetwork]:
        return self.__networks[role]

    def get_all(self) -> list[INetwork]:
        return [
            network for networks in self.__networks.values() for network in networks
        ]

    def upsert(self, role: str, network: INetwork) -> None:
        self.__networks[role].append(network)
