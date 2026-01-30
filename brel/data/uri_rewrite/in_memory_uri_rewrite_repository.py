"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 10 April 2025

====================
"""

from brel.data.uri_rewrite.uri_rewrite_repository import URIRewriteRepository


class InMemoryURIRewriteRepository(URIRewriteRepository):
    def __init__(self):
        self.__catalog = {}

    def upsert(self, original_string: str, replacement_string: str) -> None:
        self.__catalog[original_string] = replacement_string

    def delete(self, original_string: str):
        del self.__catalog[original_string]

    def rewrite(self, uri: str) -> str:
        for original_string, replacement_string in self.__catalog.items():
            if uri.startswith(original_string):
                return replacement_string + uri[len(original_string) :]

        return uri
