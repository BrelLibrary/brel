"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

import re
import urllib.parse
from lxml.etree import _ElementTree  # type: ignore
import urllib

from brel.data.xml.xml_repository import XMLRepository
from brel.services.file.file_service import FileService
from brel.services.xml.xml_file_parser_resolver import XMLFileParserResolver


class XMLService:
    def __init__(
        self,
        file_service: FileService,
        xml_repository: XMLRepository,
        parser_resolver: XMLFileParserResolver,
    ) -> None:
        self.__file_service = file_service
        self.__xml_repository = xml_repository
        self.__parser_resolver = parser_resolver

    def add_etree_recursive(self, uri: str, referencing_uri: str = ".") -> None:
        """
        Recursively adds an XML file to the repository. the uri can be a local file path or a remote URL.
        If the file is remote, it will be downloaded and added to the repository.
        The method recursively adds all referenced files to the repository.
        :param uri: The URI of the XML file to add.
        :param referencing_uri: The URI of the file that references this XML file.
        the referencing_uri is useful if a remote file references local files (e.g. http://example.com/file.xml has a reference to other_file.xml)

        """
        is_uri_remote = uri.startswith("http") or referencing_uri.startswith("http")

        uri = urllib.parse.urljoin(referencing_uri, uri)
        if self.__xml_repository.has_etree(uri):
            return

        parser = self.__parser_resolver.get_parser(uri)

        if self.__file_service.has_file(uri):
            with self.__file_service.get_file(uri) as file:
                self.__xml_repository.add_etree(uri, parser(file))
            with self.__file_service.get_file(uri) as file:
                for reference_uri in self.__extract_references(file.read()):
                    self.add_etree_recursive(reference_uri, referencing_uri=uri)

        elif is_uri_remote:
            with self.__file_service.download_and_add_file(uri) as file:
                self.__xml_repository.add_etree(uri, parser(file))
            with self.__file_service.download_and_add_file(uri) as file:
                for reference_uri in self.__extract_references(file.read()):
                    self.add_etree_recursive(reference_uri, referencing_uri=uri)

        else:
            local_filepath = urllib.parse.urlparse(uri).path
            with self.__file_service.copy_and_add_file(local_filepath) as file:
                self.__xml_repository.add_etree(uri, parser(file))
            with self.__file_service.copy_and_add_file(local_filepath) as file:
                for reference_uri in self.__extract_references(file.read()):
                    self.add_etree_recursive(reference_uri, referencing_uri=uri)

    def __extract_references(self, content: bytes) -> set[str]:
        reference_uris: set[str] = set()
        reference_pattern = re.compile(
            r":href=['\"]([^'\"]+)['\"]|schemaLocation=['\"]([^'\"]+)['\"]"
        )

        for match in reference_pattern.finditer(content.decode("utf-8")):
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

    def get_etree(self, uri: str) -> _ElementTree:
        return self.__xml_repository.get_etree(uri)

    def get_all_etrees(self) -> list[_ElementTree]:
        return self.__xml_repository.get_all_etrees()
