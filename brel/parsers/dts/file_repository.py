"""
This module is responsible for abstracting the file system. 
It downloads and caches files from the internet and the local file system.

=================

- author: Robin Schmidiger
- version: 0.2
- date: 7 April 2025

=================
"""

import urllib.parse
import fs
import fs.copy
import fs.osfs
import requests
import time
import urllib
import re
from brel.parsers.dts.file_utils import uri_to_filename
from typing import IO


class FileRepository:
    def __init__(
        self,
        session: requests.Session,
        cache_location: str,
        entrypoint_filepaths: list[str],
        clear_cache: bool = True,
    ) -> None:
        """
        Initialize the FileRepository. The repository will download and store all files that are in the transitive closure of the given entry points and their references.
        Args:
            cache_location (str): The location where the cache will be stored.
            entrypoint_filepaths (list[str]): The list of filepaths to start the repository traversal from.
        Returns:
            None
        """
        if len(entrypoint_filepaths) < 1:
            raise ValueError(
                "No filepaths provided. Make sure to provide at least one filepath."
            )

        self.fs = fs.open_fs(cache_location, create=True)
        if clear_cache:
            self.fs.removetree("/")

        self.__session = session
        self.__uris: set[str] = set()

        for file_name in entrypoint_filepaths:
            self.__fetch_and_store_recursive(file_name)

    def get_file(self, uri: str) -> IO[bytes]:
        """
        Retrieve a file from the file repository.
        This method checks if the given URI is present in the internal URI list.
        If the URI is not present, it fetches and stores the file recursively.
        Then, it converts the URI to a filename and opens the file in read-binary mode.
        Args:
            uri (str): The URI of the file to retrieve.
        Returns:
            file object: The file object opened in read-binary mode.
        """

        if uri not in self.__uris:
            self.__fetch_and_store_recursive(uri)

        file_name = uri_to_filename(uri)
        return self.fs.open(file_name, "rb")

    def get_uris(self) -> set[str]:
        """
        Retrieve the set of all reachable URIs in the repository.
        A URI is reachable if it is in the transitive closure of all references from any file in the repository.
        Returns:
            set[str]: A set containing URI strings.
        """

        return self.__uris

    def __fetch_and_store_recursive(
        self,
        uri,
        referencing_uri: str = ".",
    ):
        is_uri_remote = uri.startswith("http") or referencing_uri.startswith("http")

        uri = urllib.parse.urljoin(referencing_uri, uri)
        if uri in self.__uris:
            return
        else:
            self.__uris.add(uri)

        file_name = uri_to_filename(uri)

        if is_uri_remote:
            self.__fetch_and_store(uri, file_name)
        elif not self.fs.exists(file_name):
            try:
                parsed_uri = urllib.parse.urlparse(uri)
                local_path = parsed_uri.path
                fs.copy.copy_file(fs.osfs.OSFS("/"), local_path, self.fs, file_name)

            except FileNotFoundError:
                raise fs.errors.ResourceNotFound(
                    f"Local file '{local_path}' not found."
                )

        with self.fs.open(file_name, "rb") as f:
            for reference_uri in self.__extract_references(f.read()):
                self.__fetch_and_store_recursive(reference_uri, referencing_uri=uri)

    def __fetch_and_store(self, uri: str, file_name: str) -> None:
        try:
            headers = {}

            if "www.sec.gov" in uri:
                headers = {
                    "User-Agent": "Robin Schmidiger rschmidiger64@gmail.com",
                    "Accept-Encoding": "gzip",
                    "Host": "www.sec.gov",
                }
                time.sleep(0.1)

            response = self.__session.get(uri, headers=headers, timeout=10)
        except ConnectionError:
            raise Exception(
                f"Could not connect to {uri}. Are you connected to the internet?"
            )

        if response.status_code != 200:
            raise Exception(
                f"Failed to download {uri}. The server responded with status code {response.status_code}"
            )
        xsd_content = response.content

        with self.fs.open(file_name, "wb") as f:
            f.write(xsd_content)

    def __extract_references(self, file_binary_content: bytes) -> set[str]:
        reference_uris: set[str] = set()
        combined_pattern = re.compile(r':href="([^"]+)"|schemaLocation="([^"]+)"')
        xsd_content_str = file_binary_content.decode("utf-8", errors="ignore")
        for match in combined_pattern.finditer(xsd_content_str):
            href = match.group(1)

            if href:
                if "#" in href:
                    href_uri, _ = href.split("#")
                else:
                    href_uri = href

                if href_uri:
                    reference_uris.add(href_uri)

                schema_location = match.group(2)
                if schema_location:
                    reference_uris.add(schema_location)

        return reference_uris
