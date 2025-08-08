"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 April 2025

====================
"""

from abc import ABC, abstractmethod
from typing import List, Type
from brel.networks.i_network import INetwork


# TODO: not finalized yet. role is probably not just a string, upsert might be an update/insert instead, there should be a getter that does not return a whole list, just a single network
class NetworkRepository(ABC):
    @abstractmethod
    def get_by_type(self, role: Type[INetwork]) -> List[INetwork]:
        pass

    @abstractmethod
    def get_by_linkrole(self, linkrole: str) -> list[INetwork]:
        pass

    @abstractmethod
    def get_all(self) -> List[INetwork]:
        pass

    @abstractmethod
    def upsert(self, network: INetwork) -> None:
        pass
