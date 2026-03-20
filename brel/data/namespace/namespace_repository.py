"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 30 April 2025

====================
"""

from abc import ABC, abstractmethod


class NamespaceRepository(ABC):
    @abstractmethod
    def upsert(self, prefix: str, uri: str) -> None:
        """Insert or update a namespace."""
        pass

    @abstractmethod
    def get_uris(self, prefix: str) -> set[str]:
        """Get the URL for a given prefix."""
        pass

    @abstractmethod
    def get_prefixes(self, uri: str) -> set[str]:
        """Get the prefix for a given URL."""
        pass
