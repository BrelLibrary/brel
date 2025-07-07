"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 7 June 2025

====================
"""

from abc import ABC, abstractmethod
from typing import Any


class HrefRepository(ABC):
    @abstractmethod
    def upsert(self, base_uri: str, element_id: str, object: Any) -> None:
        """Insert or update an object with a base URI and element ID."""
        pass

    @abstractmethod
    def get_by_href(self, base_uri: str, element_id: str) -> Any:
        """Retrieve an object by its base URI and element ID."""
        pass
