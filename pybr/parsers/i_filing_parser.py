from abc import ABC, abstractmethod
from time import time

from pybr import QName, BrelLabel, PyBRFact, PyBRComponent
from pybr.reportelements import IReportElement
from pybr.networks import INetwork

from typing import final

# Implemented as an abstract class
class IFilingParser(ABC):
    """ 
    Interface for a XBRL filing parser. 
    Requires implementation of the following methods:
    - parse() -> dict
    - get_filing_type() -> str
    - parse_facts() -> Iterator[PyBRFact]
    - parse_concepts() -> Iterator[PyBRConcept]
    """
    def __print(self, output: str):
        """
        Print a message with the prefix [IFilingParser].
        """
        print_prefix = "[Parser]"
        print(print_prefix, output)

    @final
    def parse(self) -> dict:
        """
        Parse the filing.
        """
        self.__print("Parsing Labels")
        parser_start_time = time()
        labels = self.parse_labels()
        self.__print(f"took {time() - parser_start_time:.2f} sec")

        self.__print("Parsing Report Elements")
        start_time = time()
        report_elements = self.parse_report_elements(labels)
        self.__print(f"took {time() - start_time:.2f} sec")

        self.__print("Parsing Networks")
        start_time = time()
        networks = self.parse_networks(report_elements)
        self.__print(f"took {time() - start_time:.2f} sec")
        
        self.__print("Parsing Components")
        start_time = time()
        components, report_elements = self.parse_components(report_elements, networks)
        self.__print(f"took {time() - start_time:.2f} sec")
        
        self.__print("Parsing Facts")
        start_time = time()
        facts = self.parse_facts(report_elements)
        self.__print(f"took {time() - start_time:.2f} sec")
        
        self.__print(f"Done Parsing (took {time() - parser_start_time:.2f} sec)")
        filing_type = self.get_filing_type()

        networks_flattened = [network for networks_list in networks.values() for network in networks_list]

        parser_result = {
            "report elements": report_elements.values(),
            "networks": networks_flattened,
            "components": components,
            "labels": labels,
            "facts": facts,
            "filing_type": filing_type
        }

        return parser_result

    @abstractmethod
    def get_filing_type(self) -> str:
        """
        Get the filing type.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_report_elements(self, labels: dict[QName, list[BrelLabel]]) -> dict[QName, IReportElement]:
        """
        Parse the report elements.
        @param labels: A dictionary that associates SOME report element QNames with a list of labels.
        @return: A dictionary that associates ALL report element QNames with a report element object.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_facts(self, report_elements: dict[QName, IReportElement]) -> list[PyBRFact]:
        """
        Parse the facts.
        @param report_elements: A dictionary containing ALL report elements that the facts report against.
        @return: A list of facts.
        @hint: for each key,value pair in report_elements, key == value.get_name() MUST hold. 
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_networks(self, report_elements: dict[QName, IReportElement]) -> dict[str, list[INetwork]]:
        """
        Parse the networks.
        @param report_elements: A dictionary containing ALL report elements that the networks report against.
        @return: A dictionary that associates the component name with a list of networks.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_components(self, report_elements: dict[QName, IReportElement], networks: dict[str, list[INetwork]]) -> tuple[list[PyBRComponent], dict[QName, IReportElement]]:
        """
        Parse the components. Update the report elements accordingly.
        @param report_elements: A dictionary containing ALL report elements that the components report against.
        @return: A tuple containing a list of components and a dictionary containing the updated report elements.
        @hint: LineItems report elements only become LineItems if they are in LineItems positions in the components.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_labels(self) -> dict[QName, list[BrelLabel]]:
        """
        Parse the labels.
        @return: A dictionary that associates report element QNames with a list of labels.
        """
        raise NotImplementedError
