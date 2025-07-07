"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 7 June 2025

====================
"""

from typing import Any, Dict, Tuple
from brel.data.href.href_repository import HrefRepository


class InMemoryHrefRepository(HrefRepository):
    def __init__(self) -> None:
        self.__href_cache: Dict[Tuple[str, str], Any] = {}

    def upsert(self, base_uri: str, element_id: str, object: Any) -> None:
        self.__href_cache[(base_uri, element_id)] = object

    def get_by_href(self, base_uri: str, element_id: str) -> Any:
        return self.__href_cache.get((base_uri, element_id), None)
