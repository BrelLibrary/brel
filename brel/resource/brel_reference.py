"""
This module contains the BrelReference class, which represents a reference in XBRL.

=================

- author: Robin Schmidiger
- version: 0.3
- date: 19 February 2024

=================
"""

from brel.resource import IResource


class BrelReference(IResource):
    """
    Represents a Reference in XBRL.
    References are used to link to external resources such as legal documents.
    """

    def __init__(self, content: dict, label: str, role: str) -> None:
        self.__content: dict = content
        self.__role: str = role
        self.__label: str = label

    def __str__(self) -> str:
        return str(self.__content)

    # first class citizens
    def get_role(self) -> str:
        return self.__role

    def get_label(self) -> str:
        return self.__label

    def get_title(self) -> str | None:
        return None

    def get_content(self) -> dict:
        return self.__content
