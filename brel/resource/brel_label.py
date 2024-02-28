"""
This module contains the BrelLabel class, which represents a label in XBRL.

=================

- author: Robin Schmidiger
- version: 0.5
- date: 19 February 2024

=================
"""

from enum import Enum
from typing import cast

import lxml
import lxml.etree

from brel import QName, QNameNSMap
from brel.resource import IResource


class BrelLabel(IResource):
    """Represents a label in XBRL."""

    STANDARD_LABEL_ROLE = "http://www.xbrl.org/2003/role/label"

    def __init__(
        self,
        text: str,
        label: str,
        language: str,
        label_role: str = STANDARD_LABEL_ROLE,
    ) -> None:
        self.__text: str = text
        self.__language: str = language
        self.__label_role: str = label_role
        # Note: the Brellabel's label is not the same as the Brellabel's text.
        # BrelLabels with different roles can have different texts, but the same label.
        self.__label: str = label

    def __str__(self) -> str:
        return self.__text

    # first class citizens
    def get_language(self) -> str:
        return self.__language

    def get_label_role(self) -> str:
        return self.__label_role

    def get_label(self) -> str:
        return self.__label

    def get_role(self) -> str:
        return self.__label_role

    def get_title(self) -> str | None:
        return None

    def get_content(self) -> str:
        return self.__text
