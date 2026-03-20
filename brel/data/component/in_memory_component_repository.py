"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from brel.data.component.component_repository import ComponentRepository
from brel.brel_component import Component


class InMemoryComponentRepository(ComponentRepository):
    def __init__(self) -> None:
        self.__components: list[Component] = []

    def get_all(self) -> list[Component]:
        return self.__components

    def upsert(self, component: Component) -> None:
        if component in self.__components:
            self.__components.remove(component)

        self.__components.append(component)
