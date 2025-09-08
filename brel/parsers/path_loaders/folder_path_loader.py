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
        Loads all files from the specified directory recursively.

        :param path: The directory path to load files from.
        :returns: A list of file paths in the directory that are either .xml or .xhtml files.
        """
        splitting_char = "/" if "/" in path else "\\"

        path_parts = path.split(splitting_char)
        files_and_folders = [
            "/".join(path_parts + [dir_item]) for dir_item in os.listdir(path)
        ]

        files = [
            file_or_folder
            for file_or_folder in files_and_folders
            if os.path.isfile(file_or_folder)
        ]
        filtered_files = [
            file
            for file in files
            if file.endswith((".xml", ".xhtml", ".htm", "html", ".xsd"))
        ]

        folders = [
            file_or_folder
            for file_or_folder in files_and_folders
            if os.path.isdir(file_or_folder)
        ]
        subdir_file_lists = [self.load(folder) for folder in folders]

        all_files = filtered_files
        for subdir_file_list in subdir_file_lists:
            all_files.extend(subdir_file_list)

        return all_files
