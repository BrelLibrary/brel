from abc import ABC, abstractmethod
from typing import Iterator
from pybr import PyBRContext, PyBRConcept, PyBRUnit, PyBRAspect, PyBRFact

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
    def parse_facts(self) -> list[PyBRFact]:
        """
        Parse the facts.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_concepts(self) -> list[PyBRConcept]:
        """
        Parse the concepts.
        """
        raise NotImplementedError
