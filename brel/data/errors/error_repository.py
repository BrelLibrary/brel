"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from abc import ABC, abstractmethod
from typing import Callable, final


class ErrorRepository(ABC):
    @abstractmethod
    def upsert(self, error: Exception) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[Exception]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @final
    def upsert_on_error[T](self, expression: Callable[[], T]) -> T | None:
        try:
            return expression()
        except Exception as e:
            self.upsert(e)
            return None

    @final
    def upsert_if(self, condition: bool, error: Exception) -> None:
        if condition:
            self.upsert(error)

    def get_by_type(self, error_type: type[Exception]) -> list[Exception]:
        return [error for error in self.get_all() if isinstance(error, error_type)]
