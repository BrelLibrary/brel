"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from typing import List
from abc import ABC, abstractmethod
from brel.brel_component import Component


class ComponentRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Component]:
        pass

    @abstractmethod
    def upsert(self, component: Component) -> None:
        pass
