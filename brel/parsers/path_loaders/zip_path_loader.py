"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

from brel.parsers.path_loaders.path_loader import PathLoader


class ZipPathLoader(PathLoader):
    def is_loader_for(self, path: str) -> bool:
        return path.endswith(".zip")

    def load(self, path: str) -> list[str]:
        import zipfile

        with zipfile.ZipFile(path, "r") as zip_ref:
            file_list = zip_ref.namelist()
            return [file for file in file_list if file.endswith((".xml", ".xhtml"))]
