"""
====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 May 2025

====================
"""

from abc import ABC, abstractmethod


class URIRewriteRepository(ABC):
    @abstractmethod
    def upsert(self, original_string: str, replacement_string: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, original_string: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def rewrite(self, uri: str) -> str:
        raise NotImplementedError
