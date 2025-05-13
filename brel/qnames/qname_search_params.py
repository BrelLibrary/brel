"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class QNameSearchParams:
    local_name: str
    uri: str | None = None
    prefix: str | None = None

    @staticmethod
    def is_clark_notation(clark_notation: str) -> bool:
        """
        Check if the given string is in Clark notation.
        """
        re_expression = r"^(?P<prefix>[^:]+):(?P<local_name>[^:]+)$"
        match = re.match(re_expression, clark_notation)
        return match is not None

    @classmethod
    def from_clark_notation(cls, clark_notation: str) -> "QNameSearchParams":
        """
        Create a QNameSearchParams object from a Clark notation string.
        """
        re_expression = r"^(?P<prefix>[^:]+):(?P<local_name>[^:]+)$"
        match = re.match(re_expression, clark_notation)
        if not match:
            raise ValueError(
                f"Invalid Clark notation: {clark_notation}. Expected format: prefix:local_name"
            )
        prefix = match.group("prefix")
        local_name = match.group("local_name")
        uri = None
        return cls(local_name=local_name, uri=uri, prefix=prefix)

    @staticmethod
    def is_prefix_local_name_notation(prefix_local_name: str) -> bool:
        """
        Check if the given string is in prefix-localname notation.
        """
        re_expression = r"^(?P<prefix>[^:]+):(?P<local_name>[^:]+)$"
        match = re.match(re_expression, prefix_local_name)
        return match is not None

    @classmethod
    def from_prefix_local_name_notation(
        cls, prefix_localname: str
    ) -> "QNameSearchParams":
        """
        Create a QNameSearchParams object from a prefix and local name string.
        """
        re_expression = r"^(?P<prefix>[^:]+):(?P<local_name>[^:]+)$"
        match = re.match(re_expression, prefix_localname)
        if not match:
            raise ValueError(
                f"Invalid prefix-localname notation: {prefix_localname}. Expected format: prefix:local_name"
            )
        prefix = match.group("prefix")
        local_name = match.group("local_name")
        uri = None
        return cls(local_name=local_name, uri=uri, prefix=prefix)

    @classmethod
    def from_string(cls, qname_search_str: str) -> "QNameSearchParams":
        """
        Create a QNameSearchParams object from a string.
        """
        if cls.is_clark_notation(qname_search_str):
            return cls.from_clark_notation(qname_search_str)
        elif cls.is_prefix_local_name_notation(qname_search_str):
            return cls.from_prefix_local_name_notation(qname_search_str)
        else:
            return cls(local_name=qname_search_str, uri=None, prefix=None)
