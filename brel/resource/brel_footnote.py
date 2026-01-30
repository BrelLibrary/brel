"""
This module contains the BrelFootnote class, which represents a footnote in XBRL.

=================

- author: Robin Schmidiger
- version: 0.3
- date: 19 February 2024

=================
"""

from brel.resource import IResource
from typing import Optional, cast


class BrelFootnote(IResource):
    """
    Represents a Reference in XBRL.
    References are used to link to external resources such as legal documents.
    """

    def __init__(
        self,
        content: str,
        label: str,
        language: str,
        role: str,
        id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        self.__content: str = content
        self.__role: str = role
        self.__language: str = language
        self.__label: str = label
        self.__id: Optional[str] = id
        self.__title: Optional[str] = title

    def __str__(self) -> str:
        return str(self.__content)

    # first class citizens
    def get_id(self) -> Optional[str]:
        return self.__id

    def get_role(self) -> str:
        return self.__role

    def get_label(self) -> str:
        return self.__label

    def get_title(self) -> Optional[str]:
        return self.__title

    def get_content(self) -> str:
        return self.__content

    def get_language(self) -> str:
        """
        :returns str: the language of the footnote
        """
        return self.__language
