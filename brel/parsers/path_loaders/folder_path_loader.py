"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

import os

from brel.parsers.path_loaders.path_loader import PathLoader


class FolderPathLoader(PathLoader):
    def is_loader_for(self, path: str) -> bool:
        """
        Checks if the loader is applicable for the given path.
        This loader is applicable for any directory path.
        Does not work for web links.
        :param path: The directory path to check.
        :returns: True if the loader can handle the path, False otherwise.
        """
        return os.path.isdir(path)

    def load(self, path: str) -> list[str]:
        """
        Loads all files from the specified directory.

        :param path: The directory path to load files from.
        :returns: A list of file paths in the directory that are either .xml or .xhtml files.
        """
        return [
            os.path.join(path, file)
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
            and file.endswith((".xml", ".xhtml"))
        ]
