"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 30 April 2025

====================
"""


from collections import defaultdict
from brel.data.namespace.namespace_repository import NamespaceRepository


class InMemoryNamespaceRepository(NamespaceRepository):
    def __init__(self) -> None:
        self.__prefix_to_url: dict[str, set[str]] = defaultdict(set)
        self.__uri_to_prefix: dict[str, set[str]] = defaultdict(set)

    def upsert(self, prefix: str, uri: str) -> None:
        self.__prefix_to_url[prefix].add(uri)
        self.__uri_to_prefix[uri].add(prefix)

    def get_uris(self, prefix: str) -> set[str]:
        return self.__prefix_to_url.get(prefix, set())

    def get_prefixes(self, uri: str) -> set[str]:
        return self.__uri_to_prefix.get(uri, set())
