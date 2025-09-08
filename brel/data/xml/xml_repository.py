"""
This module contains the XMLSchemaManager class.
The XMLSchemaManager class is responsible for downloading and caching XBRL taxonomies.

=================

- author: Robin Schmidiger
- version: 0.9
- date: 07 April 2025

=================
"""

import lxml
import lxml.etree
from brel.parsers.utils.lxml_xpath_utils import add_xpath_functions


class XMLRepository:
    def __init__(self) -> None:
        self.__xml_etree_cache: dict[str, lxml.etree._ElementTree] = {}
        add_xpath_functions()

    def normalize_uri(self, uri: str) -> str:
        if uri.startswith("http"):
            return uri
        
        return uri.replace("\\", "/")

    def has_etree(self, uri: str) -> bool:
        return self.normalize_uri(uri) in self.__xml_etree_cache

    def get_etree(self, uri: str) -> lxml.etree._ElementTree:
        return self.__xml_etree_cache[self.normalize_uri(uri)]

    def get_all_etrees(self) -> list[lxml.etree._ElementTree]:
        return list(self.__xml_etree_cache.values())

    def add_etree(self, uri: str, etree: lxml.etree._ElementTree) -> None:
        self.__xml_etree_cache[self.normalize_uri(uri)] = etree
