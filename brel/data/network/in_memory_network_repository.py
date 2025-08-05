"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 2 April 2025

====================
"""

from collections import defaultdict
from typing import Type
from brel.data.network.network_repository import NetworkRepository
from brel.networks.i_network import INetwork


class InMemoryNetworkRepository(NetworkRepository):
    def __init__(self) -> None:
        self.__networks: dict[Type[INetwork], list[INetwork]] = defaultdict(list)

    def get(self, role: Type[INetwork]) -> list[INetwork]:
        return self.__networks[role]
    
    def get_all(self) -> list[INetwork]:
        return [
            network for networks in self.__networks.values() for network in networks
        ]

    def upsert(self, network: INetwork) -> None:
        self.__networks[type(network)].append(network)
