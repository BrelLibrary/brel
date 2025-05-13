"""
====================

- author: Robin Schmidiger
- version: 0.7
- date: 2 May 2025

====================
"""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class QName:
    uri: str
    prefix: str
    local_name: str

    def get_URL(self) -> str:
        return self.uri

    def get_prefix(self) -> str:
        return self.prefix

    def get_local_name(self) -> str:
        return self.local_name

    def clark_notation(self) -> str:
        """
        :returns str: containing the clark notation of the qualified name
        """
        return f"{{{self.uri}}}{self.local_name}"

    def prefix_local_name_notation(self) -> str:
        """
        :returns str: containing the prefix:localname notation of the qualified name
        """
        return f"{self.prefix}:{self.local_name}"

    def __str__(self) -> str:
        """
        :returns str: containing the clark notation of the qualified name
        """
        return self.prefix_local_name_notation()
