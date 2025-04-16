"""
====================

- author: Robin Schmidiger
- version: 0.2
- date: 15 April 2025

====================
"""

from abc import ABC, abstractmethod
from brel.brel_fact import Fact


class FactRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Fact:
        pass

    @abstractmethod
    def has_id(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> list[Fact]:
        pass

    @abstractmethod
    def upsert(self, fact: Fact) -> None:
        pass
