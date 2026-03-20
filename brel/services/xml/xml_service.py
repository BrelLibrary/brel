"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

import re
from typing import List, Optional, Set
import urllib.parse
from lxml.etree import _ElementTree  # type: ignore
import urllib

from brel.data.uri_rewrite.uri_rewrite_repository import URIRewriteRepository
from brel.data.xml.xml_repository import XMLRepository
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.services.file.file_service import FileService
from brel.services.xml.xml_file_parser_resolver import XMLFileParserResolver


class XMLService:
    def __init__(
        self,
        file_service: FileService,
        xml_repository: XMLRepository,
        uri_rewrite_repository: URIRewriteRepository,
        parser_resolver: XMLFileParserResolver,
    ) -> None:
        self.__file_service = file_service
        self.__uri_rewrite_repository = uri_rewrite_repository
        self.__xml_repository = xml_repository
        self.__parser_resolver = parser_resolver
        self.__available_filing_languages: Optional[List[str]] = None

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
        if not is_uri_remote:
            referencing_splitting_char = "\\" if "\\" in referencing_uri else "/"
            uri_splitting_char = "\\" if "\\" in uri else "/"

            uri = uri_splitting_char.join(
                referencing_uri.split(referencing_splitting_char)[:-1]
                + uri.split(uri_splitting_char)
            )
        else:
            uri = urllib.parse.urljoin(referencing_uri, uri)

        uri = self.__uri_rewrite_repository.rewrite(uri)
        is_uri_remote = uri.startswith("http") or referencing_uri.startswith("http")

        if self.__xml_repository.has_etree(uri):
            return

        parser = self.__parser_resolver.get_parser(uri)

        if self.__file_service.has_file(uri):
            with self.__file_service.get_file(uri) as file:
                self.__xml_repository.add_etree(uri, parser(file))
        elif is_uri_remote:
            with self.__file_service.download_and_add_file(uri) as file:
                self.__xml_repository.add_etree(uri, parser(file))
        else:
            local_filepath = urllib.parse.urlparse(uri).path
            with self.__file_service.copy_and_add_file(local_filepath) as file:
                self.__xml_repository.add_etree(uri, parser(file))

        with self.__file_service.get_file(uri) as file:
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
                # get only last part, as there can be 2 links, only the second of which is relevant in our case.
                schema_location = schema_location.split()[-1]
                reference_uris.add(schema_location)

        return reference_uris

    def get_etree(self, uri: str) -> _ElementTree:
        return self.__xml_repository.get_etree(uri)

    def get_all_etrees(self) -> list[_ElementTree]:
        return self.__xml_repository.get_all_etrees()

    def get_available_filing_languages(self) -> List[str]:
        if self.__available_filing_languages is None:
            all_languages: Set[str] = set()
            for tree in self.get_all_etrees():
                elements_with_lang = tree.findall(
                    "//*[@xml:lang]", {"xml": "http://www.w3.org/XML/1998/namespace"}
                )

                tree_languages = set(
                    get_str_attribute(element_with_lang, "xml:lang")
                    for element_with_lang in elements_with_lang
                )

                all_languages = all_languages.union(tree_languages)

            self.__available_filing_languages = list(all_languages)

        return self.__available_filing_languages
