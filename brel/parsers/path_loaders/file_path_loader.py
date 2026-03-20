"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

import os
from brel.parsers.path_loaders.path_loader import PathLoader


class FilePathLoader(PathLoader):
    def is_loader_for(self, path: str) -> bool:
        """
        Checks if the loader is applicable for the given path.
        This loader is applicable for any file path that is not a directory.
        The supported file extensions are: .xml and .xhtml.
        Weblinks are also supported.
        :param path: The file path to check.
        :returns: True if the loader can handle the path, False otherwise.
        """
        if path.endswith((".xml", ".xhtml")):
            if os.path.isfile(path):
                return True
            if path.startswith(("http://", "https://")):
                return True
        return False

    def load(self, path: str) -> list[str]:
        """
        Loads a single file.

        :param path: The file path to load.
        :returns: A list containing the file path.
        """
        return [path]
