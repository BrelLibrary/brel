"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from brel.data.errors.error_repository import ErrorRepository


class InMemoryErrorRepository(ErrorRepository):
    def __init__(self) -> None:
        self.errors: list[Exception] = []

    def upsert(self, error: Exception) -> None:
        self.errors.append(error)

    def get_all(self) -> list[Exception]:
        return self.errors

    def clear(self) -> None:
        self.errors.clear()
