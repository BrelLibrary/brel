"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 08 May 2025

====================
"""


from abc import ABC, abstractmethod
from typing import IO


class FileRepository(ABC):
    @abstractmethod
    def get_file(self, uri: str) -> IO[bytes]:
        pass

    @abstractmethod
    def has_file(self, uri: str) -> bool:
        pass

    @abstractmethod
    def add_file(self, uri: str, file: IO[bytes]) -> None:
        pass
