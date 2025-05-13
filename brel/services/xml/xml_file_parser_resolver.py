"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from typing import IO, Callable, Dict
from lxml.etree import _ElementTree  # type: ignore


class XMLFileParserResolver:
    def __init__(
        self,
        xml_parser: Callable[[IO[bytes]], _ElementTree],
        xhtml_parser: Callable[[IO[bytes]], _ElementTree],
    ):
        self.__parsers: Dict[str, Callable[[IO[bytes]], _ElementTree]] = {
            ".xml": xml_parser,
            ".xsd": xml_parser,
            ".xhtml": xhtml_parser,
        }

    def get_parser(self, file_name: str) -> Callable[[IO[bytes]], _ElementTree]:
        for ext, parser in self.__parsers.items():
            if file_name.endswith(ext):
                return parser
        raise ValueError(f"No parser registered for: {file_name}")
