"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 08 May 2025

====================
"""


import time
from io import BytesIO
from typing import IO
from requests import Session
from brel.data.file.file_repository import FileRepository


class FileService:
    def __init__(self, file_repository: FileRepository, session: Session) -> None:
        self.__file_repository = file_repository
        self.__session = session

    def add_file(self, uri: str, file: IO[bytes]) -> None:
        self.__file_repository.add_file(uri, file)

    def get_file(self, uri: str) -> IO[bytes]:
        return self.__file_repository.get_file(uri)

    def has_file(self, uri: str) -> bool:
        return self.__file_repository.has_file(uri)

    def download_and_add_file(self, uri: str) -> IO[bytes]:
        headers = {}

        if "www.sec.gov" in uri:
            headers = {
                "User-Agent": "Robin Schmidiger rschmidiger64@gmail.com",
                "Accept-Encoding": "gzip",
                "Host": "www.sec.gov",
            }
            time.sleep(0.1)

        response = self.__session.get(uri, headers=headers, timeout=10)
        response.raise_for_status()
        file = BytesIO(response.content)
        self.add_file(uri, file)
        return self.get_file(uri)

    def copy_and_add_file(self, local_path: str) -> IO[bytes]:
        with open(local_path, "rb") as file:
            self.add_file(local_path, file)
        return self.get_file(local_path)
