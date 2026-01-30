"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""
from lxml import etree
from abc import ABC, abstractmethod
from typing import Callable, Optional, final

from brel.errors.error_factory_registry import error_factory_registry
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.errors.severity import Severity


class ErrorRepository(ABC):
    @abstractmethod
    def insert_premade(self, error: ErrorInstance) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[ErrorInstance]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    def create(
        cls,
        error_code: ErrorCode,
        error_context: Optional[etree._Element] = None,
        **kwargs: Optional[str],
    ) -> ErrorInstance:
        error_instance_factory = error_factory_registry.get(error_code)
        if not error_instance_factory:
            raise ValueError(f"Error code {error_code} is not valid.")

        error_instance = error_instance_factory()
        error_instance.update_message(**kwargs)
        if error_context is not None:
            error_instance.set_context(error_context)

        return error_instance

    @final
    def insert(
        self,
        error_code: ErrorCode,
        error_context: Optional[etree._Element] = None,
        **kwargs: Optional[str],
    ) -> None:
        error_instance = self.create(error_code, error_context, **kwargs)
        self.insert_premade(error_instance)

    @final
    def upsert_if(self, condition: bool, error: ErrorInstance) -> None:
        if condition:
            self.insert_premade(error)

    @final
    def get_by_severity(self, severity: Severity) -> list[ErrorInstance]:
        return [error for error in self.get_all() if error.get_severity() == severity]
