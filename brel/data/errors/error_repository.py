"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from abc import ABC, abstractmethod
from typing import Callable, final

from brel.errors.error_instance import ErrorInstance
from brel.errors.severity import Severity


class ErrorRepository(ABC):
    @abstractmethod
    def upsert(self, error: ErrorInstance) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[ErrorInstance]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @final
    def upsert_on_error[
        T
    ](self, expression: Callable[[], T], error: ErrorInstance) -> T | None:
        try:
            return expression()
        except Exception:
            self.upsert(error)
            return None

    @final
    def upsert_if(self, condition: bool, error: ErrorInstance) -> None:
        if condition:
            self.upsert(error)

    def get_by_severity(self, severity: Severity) -> list[ErrorInstance]:
        return [error for error in self.get_all() if error.get_severity() == severity]
