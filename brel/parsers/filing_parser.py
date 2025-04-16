"""
====================

- author: Robin Schmidiger
- version: 0.3
- date: 12 April 2025

====================
"""

from abc import ABC, abstractmethod
from typing import final


from brel.contexts.filing_context import FilingContext

DEBUG = False
LOADING_INFO = False


class FilingParser(ABC):
    """
    Interface for a XBRL filing parser.
    Requires implementation of the following methods:
    """

    def __init__(self, context: FilingContext) -> None:
        """
        Initialize the parser.
        """
        self.__context = context

    def get_context(self):
        """
        Get the context.
        """
        return self.__context

    @final
    def parse(self) -> None:
        """
        Parse the filing.
        """
        self.parse_report_elements()
        self.parse_facts()
        self.parse_networks()
        self.parse_components()

    @abstractmethod
    def get_filing_type(self) -> str:
        """
        Get the filing type.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_report_elements(self) -> None:
        """
        Parse the report elements. Even those that are not part of any network or fact.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_facts(self) -> None:
        """
        Parse the facts. Assumes that the report elements have been parsed already.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_networks(self) -> None:
        """
        Parse the networks and updates the report element lookup function accordingly. Assumes that the facts and report elements have been parsed already.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_components(self) -> None:
        """
        Parse the components. Assumes the facts, report elements and networks have been parsed already.
        """
        raise NotImplementedError
