from abc import ABC, abstractmethod
from pybr import IReportElement, PyBRFact, PyBRLabel, PyBRComponent, QName

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

    @abstractmethod
    def parse(self) -> dict:
        """
        Parse the filing.
        """
        raise NotImplementedError

    @abstractmethod
    def get_filing_type(self) -> str:
        """
        Get the filing type.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_report_elements(self) -> list[IReportElement]:
        """
        Parse the concepts.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_facts(self, report_elements: dict[QName, IReportElement]) -> list[PyBRFact]:
        """
        Parse the facts.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_components(self) -> list[PyBRComponent]:
        """
        Parse the components.
        """
        raise NotImplementedError
    
    @abstractmethod
    def parse_labels(self) -> list[PyBRLabel]:
        """
        Parse the labels.
        """
        raise NotImplementedError
