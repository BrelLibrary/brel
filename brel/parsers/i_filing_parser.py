from abc import ABC, abstractmethod
from time import time
from typing import final, Iterable, Tuple
from collections.abc import Mapping

from brel import Component, Fact, QName, QNameNSMap
from brel.networks import INetwork
from brel.reportelements import IReportElement

DEBUG = False
LOADING_INFO = False


# Implemented as an abstract class
class IFilingParser(ABC):
    """
    Interface for a XBRL filing parser.
    Requires implementation of the following methods:
    - parse() -> dict
    - get_filing_type() -> str
    - parse_facts() -> Iterator[Fact]
    - parse_concepts() -> Iterator[Concept]
    """

    def __init__(self) -> None:
        """
        Initialize the parser.
        """
        raise NotImplementedError

    def __print(self, output: str):
        """
        Print a message with the prefix [IFilingParser].
        """
        if DEBUG:  # pragma: no cover
            print_prefix = "[Parser]"
            print(print_prefix, output)

    @abstractmethod
    def get_nsmap(self) -> QNameNSMap:
        """
        Get the namespace map.
        """
        raise NotImplementedError

    @final
    def parse(self) -> dict:
        """
        Parse the filing.
        """
        parser_start_time = time()

        if LOADING_INFO:  # pragma: no cover
            print(f"Loading the filing. This may take a couple of seconds...")

        if DEBUG:  # pragma: no cover
            self.__print("Parsing Report Elements")
        start_time = time()

        report_elements = self.parse_report_elements()

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Facts")
        start_time = time()

        facts = self.parse_facts(report_elements)

        if DEBUG:
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Networks")
        start_time = time()

        networks = self.parse_networks(report_elements)

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Components")
        start_time = time()

        components = self.parse_components(networks)

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print(f"Done Parsing (took {time() - parser_start_time:.2f} sec)")
        filing_type = self.get_filing_type()

        # networks_flattened = list(networks.values())
        networks_flattened = [
            network
            for component_networks in networks.values()
            for network in component_networks
        ]

        parser_result = {
            "report elements": list(report_elements.values()),
            "networks": networks_flattened,
            "components": components,
            "facts": facts,
            "filing_type": filing_type,
            "nsmap": self.get_nsmap(),
        }

        return parser_result

    @abstractmethod
    def get_filing_type(self) -> str:
        """
        Get the filing type.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_report_elements(
        self,
    ) -> Mapping[QName, IReportElement]:
        """
        Parse the report elements.
        :returns: A lookup that, given a QName, returns the report element with that QName.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_facts(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Iterable[Fact]:
        """
        Parse the facts.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns Iterable[Fact]: A list of facts.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_networks(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Mapping[str, Iterable[INetwork]]:
        """
        Parse the networks and updates the report element lookup function accordingly.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns: A lookup function that, given a role uri, returns a list of networks with that uri.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_components(
        self,
        networks: Mapping[str, Iterable[INetwork]],
    ) -> Iterable[Component]:
        """
        Parse the components.
        :param networks: A lookup function that, given a role uri, returns a list of networks with that uri.
        :returns Iterable[Component]: A list of components.
        """
        raise NotImplementedError
