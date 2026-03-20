"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 10 April 2025

====================
"""
from brel.characteristics.brel_aspect import Aspect
from brel.data.aspect.aspect_repository import AspectRepository


class InMemoryAspectRepository(AspectRepository):
    def __init__(self) -> None:
        self.__aspects: dict[str, Aspect] = {}

    def get(self, name: str) -> Aspect:
        return self.__aspects[name]

    def has(self, name: str) -> bool:
        return name in self.__aspects

    def upsert(self, aspect: Aspect) -> None:
        self.__aspects[aspect.get_name()] = aspect
