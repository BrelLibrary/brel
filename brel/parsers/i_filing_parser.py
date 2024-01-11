from abc import ABC, abstractmethod
from time import time

from brel import QName, Fact, Component, QNameNSMap
from brel.reportelements import IReportElement
from brel.networks import INetwork

from typing import final

DEBUG = False
LOADING_INFO = True


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

    def __init__(
        self,
        instance_filename: str,
        networks_filenames: list[str],
    ) -> None:
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
        components, report_elements = self.parse_components(
            report_elements, networks
        )
        if DEBUG:  # pragma: no cover
            self.__print(f"took {time() - start_time:.2f} sec")

            self.__print(
                f"Done Parsing (took {time() - parser_start_time:.2f} sec)"
            )
        filing_type = self.get_filing_type()

        networks_flattened = [
            network
            for networks_list in networks.values()
            for network in networks_list
        ]

        parser_result = {
            "report elements": report_elements.values(),
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
    def parse_report_elements(self) -> dict[QName, IReportElement]:
        """
        Parse the report elements.
        @return: A dictionary that associates ALL report element QNames with a report element object.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_facts(
        self, report_elements: dict[QName, IReportElement]
    ) -> list[Fact]:
        """
        Parse the facts.
        @param report_elements: A dictionary containing ALL report elements that the facts report against.
        @return: A list of facts.
        @hint: for each key,value pair in report_elements, key == value.get_name() MUST hold.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_networks(
        self, report_elements: dict[QName, IReportElement]
    ) -> dict[str | None, list[INetwork]]:
        """
        Parse the networks.
        @param report_elements: A dictionary containing ALL report elements that the networks report against.
        @return: A dictionary that associates the component name with a list of networks.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_components(
        self,
        report_elements: dict[QName, IReportElement],
        networks: dict[str | None, list[INetwork]],
    ) -> tuple[list[Component], dict[QName, IReportElement]]:
        """
        Parse the components. Update the report elements accordingly.
        @param report_elements: A dictionary containing ALL report elements that the components report against.
        @return: A tuple containing a list of components and a dictionary containing the updated report elements.
        @hint: LineItems report elements only become LineItems if they are in LineItems positions in the components.
        """
        raise NotImplementedError
