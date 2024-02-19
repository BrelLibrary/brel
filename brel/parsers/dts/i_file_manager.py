"""
Contains the interface for a file manager

====================

- author: Robin Schmidiger
- version: 0.2
- date: 19 December 2023

====================
"""

from abc import ABC, abstractmethod
from typing import Any


class IFileManager(ABC):
    @abstractmethod
    def get_file(self, schema_uri: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_all_files(self) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_file_names(self) -> list[str]:
        raise NotImplementedError
