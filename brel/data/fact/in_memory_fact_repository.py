"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 9 April 2025

====================
"""

from brel.data.fact.fact_repository import FactRepository
from brel.brel_fact import Fact


class InMemoryFactRepository(FactRepository):
    def __init__(self) -> None:
        self.__facts_by_id: dict[str, Fact] = {}
        self.__facts_without_id: list[Fact] = []

    def get_by_id(self, id: str) -> Fact:
        return self.__facts_by_id[id]

    def has_id(self, id: str) -> bool:
        return id in self.__facts_by_id

    def get_all(self):
        return list(self.__facts_by_id.values())

    def upsert(self, fact: Fact) -> None:
        """
        Set the fact by its ID.
        :param fact: The fact to set.
        """
        fact_id = fact.get_id()
        if fact_id is None:
            self.__facts_without_id.append(fact)
        else:
            self.__facts_by_id[fact_id] = fact
