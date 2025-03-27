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

        errors: list[Exception] = []

        if LOADING_INFO:  # pragma: no cover
            print(f"Loading the filing. This may take a couple of seconds...")

        if DEBUG:  # pragma: no cover
            self.__print("Parsing Report Elements")
        start_time = time()

        report_elements, report_elements_errors = self.parse_report_elements()
        errors.extend(report_elements_errors)

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Facts")
        start_time = time()

        facts, facts_errors = self.parse_facts(report_elements)
        errors.extend(facts_errors)

        if DEBUG:
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Networks")
        start_time = time()

        networks, networks_errors = self.parse_networks(report_elements)
        errors.extend(networks_errors)

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print("Parsing Components")
        start_time = time()

        components, components_errors = self.parse_components(networks)
        errors.extend(components_errors)

        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print(f"Done Parsing (took {time() - parser_start_time:.2f} sec)")
        filing_type = self.get_filing_type()

        # networks_flattened = list(networks.values())
        networks_flattened = [network for component_networks in networks.values() for network in component_networks]

        parser_result = {
            "report elements": list(report_elements.values()),
            "networks": networks_flattened,
            "components": components,
            "facts": facts,
            "filing_type": filing_type,
            "nsmap": self.get_nsmap(),
            "errors": errors,
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
    ) -> Tuple[Mapping[QName, IReportElement], Iterable[Exception]]:
        """
        Parse the report elements. Even those that are not part of any network or fact.
        :returns:
        - A lookup that, given a QName, returns the report element with that QName.
        - A list of errors that occurred during parsing.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_facts(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Tuple[Iterable[Fact], Iterable[Exception]]:
        """
        Parse the facts.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns
        - Iterable[Fact]: A list of facts.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_networks(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Tuple[Mapping[str, Iterable[INetwork]], Iterable[Exception]]:
        """
        Parse the networks and updates the report element lookup function accordingly.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns:
        - Mapping[str, Iterable[INetwork]]: A lookup function that, given a role uri, returns a list of networks with that uri.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_components(
        self,
        networks: Mapping[str, Iterable[INetwork]],
    ) -> Tuple[Iterable[Component], Iterable[Exception]]:
        """
        Parse the components.
        :param networks: A lookup function that, given a role uri, returns a list of networks with that uri.
        :returns:
        - Iterable[Component]: A list of components.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        raise NotImplementedError
