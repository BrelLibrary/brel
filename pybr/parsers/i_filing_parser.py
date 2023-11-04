from abc import ABC, abstractmethod

from pybr import QName, PyBRLabel, PyBRFact, PyBRComponent
from pybr.reportelements import IReportElement

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

    @final
    def parse(self) -> dict:
        """
        Parse the filing.
        """
        labels = self.parse_labels()
        report_elements = self.parse_report_elements(labels)
        components, report_elements = self.parse_components(report_elements)
        facts = self.parse_facts(report_elements)
        filing_type = self.get_filing_type()

        parser_result = {
            "report elements": report_elements,
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
    def parse_report_elements(self, labels: dict[QName, list[PyBRLabel]]) -> dict[QName, IReportElement]:
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
    def parse_components(self, report_elements: dict[QName, IReportElement]) -> tuple[list[PyBRComponent], dict[QName, IReportElement]]:
        """
        Parse the components. Update the report elements accordingly.
        @param report_elements: A dictionary containing ALL report elements that the components report against.
        @return: A tuple containing a list of components and a dictionary containing the updated report elements.
        @hint: LineItems report elements only become LineItems if they are in LineItems positions in the components.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_labels(self) -> dict[QName, list[PyBRLabel]]:
        """
        Parse the labels.
        @return: A dictionary that associates report element QNames with a list of labels.
        """
        raise NotImplementedError
