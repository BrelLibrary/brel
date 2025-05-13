"""
This module is responsible for abstracting the file system. 
It downloads and caches files from the internet and the local file system.

=================

- author: Robin Schmidiger
- version: 0.2
- date: 7 April 2025

=================
"""

import fs
from brel.data.file.file_repository import FileRepository
from brel.parsers.utils.file_utils import uri_to_filename
from typing import IO


class PyFsFileRepository(FileRepository):
    def __init__(
        self,
        cache_location: str,
        clear_cache: bool = True,
    ) -> None:
        self.fs = fs.open_fs(cache_location, create=True)
        if clear_cache:
            self.fs.removetree("/")

    def add_file(self, uri: str, file: IO[bytes]) -> None:
        return self.fs.writetext(
            uri_to_filename(uri),
            file.read().decode("utf-8"),
        )

    def get_file(self, uri: str) -> IO[bytes]:
        file_name = uri_to_filename(uri)
        return self.fs.open(file_name, "rb")

    def has_file(self, uri: str) -> bool:
        return self.fs.exists(uri_to_filename(uri))
