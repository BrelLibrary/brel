"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

from abc import ABC, abstractmethod


class PathLoader(ABC):
    @abstractmethod
    def is_loader_for(self, path: str) -> bool:
        """
        Abstract method to check if the loader is applicable for the given path.
        :param path: The path to check.
        :return: True if the loader can handle the path, False otherwise.
        """
        pass

    @abstractmethod
    def load(self, path: str) -> list[str]:
        """
        Abstract method to load paths.
        :return: A list of paths.
        """
        pass
