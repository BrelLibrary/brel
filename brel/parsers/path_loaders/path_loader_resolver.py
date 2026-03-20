"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

from brel.parsers.path_loaders.path_loader import PathLoader


class PathLoaderResolver:
    def __init__(self, loaders: list[PathLoader]):
        self.loaders = loaders

    def get_path_loader(self, path: str) -> PathLoader:
        for loader in self.loaders:
            if loader.is_loader_for(path):
                return loader

        raise ValueError(f"No suitable loader found for path: {path}")
