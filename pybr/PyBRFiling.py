import os
import lxml
import lxml.etree
from lxml.etree import _Element as lxmlElement
# from pybr import PyBRFact, PyBRConcept, PyBRContext, PyBRUnit
from pybr.PyBRFact import PyBRFact
from pybr.PyBRConcept import PyBRConcept
from pybr.PyBRContext import PyBRContext
from pybr.PyBRUnit import PyBRUnit
from pybr import QName
from pybr.PyBRLinkbase import PyBRLinkbase
from pybr import PyBRAspect
import editdistance
from pybr.Parsers import IFilingParser, XMLFilingParser

class PyBRFiling:
    """A wrapper class for loading and manipulating a filing"""
    # TODO: Add support for more than just the instance and the schema
    """
    Idea: Instead of eagerly loading the whole filing, I load the xml files and only parse
    them to python objects when they are needed.
    So the PyBRFiling class is just a wrapper for the xml files, but its return values are
    python objects.
    """

    """
    The methods of this class are the following:
    - 1st class methods
    --> static open(FilePath | URL file_path): PyBRFiling
    --> get_all_facts(): list[PyBRFact]
    --> get_all_concepts(): list[PyBRConcept]
    --> ... (to designed)
    - 2nd class methods
    --> get_concept_by_name(concept_name: QName): PyBRConcept
    --> get_all_reported_concepts(): list[PyBRConcept]
    --> get_facts_by_concept_name(concept_name: QName): PyBRFact
    --> get_all_labels(): list[PyBRLabel]
    --> pd.DataFrame get_all_facts_as_dataframe(): pd.DataFrame
    - built-in methods
    --> __init__(self, xbrl_schema: lxmlElement, xbrl_instance: lxmlElement) (will take more parameters later)
    --> __str__(self): str
    """
    def __init__(self, parser: IFilingParser) -> None:
        self.__parser = parser

        parser_result = parser.parse()

        self.__facts = parser_result["facts"]
        self.__concepts = parser_result["concepts"]

    def get_all_facts(self) -> list[PyBRFact]:
        """Get all facts in the filing"""
        return self.__facts
    
    def get_all_concepts(self) -> list[PyBRConcept]:
        """Get all concepts in the filing"""
        return self.__concepts
    
    @classmethod
    def open(cls, folder_path):
        """Load a filing from a local folder"""
        # first check if the file path resolves to a folder
        if not os.path.isdir(folder_path):
            # TODO: Don't use exceptions. use message passing instead
            raise ValueError(f"The path {folder_path} does not resolve to a folder")
        
        # create a parser for xml
        # TODO: support parsers for json and csv. also automatically choose the right parser
        parser = XMLFilingParser(folder_path)
        
        # create a new PyBRFiling object
        new_filing = cls(parser)

        return new_filing
    
    def get_concept_by_name(self, concept_name: QName) -> PyBRConcept:
        """Get a concept by its name"""
        concept: PyBRConcept | None = None
        for c in self.__concepts:
            if c.get_name() == concept_name:
                concept = c
                break
        
        if concept is None:
            raise ValueError(f"Concept {concept_name} not found")
        
        return concept
    
    def get_all_reported_concepts(self) -> list[PyBRConcept]:
        """Get all concepts that are reported in the filing"""
        reported_concepts = []
        for fact in self.__facts:
            if fact.get_concept() not in reported_concepts:
                reported_concepts.append(fact.get_concept())
        
        return reported_concepts
    
    def get_facts_by_concept_name(self, concept_name: QName) -> list[PyBRFact]:
        """Get all facts that are associated with a concept"""
        facts = []
        for fact in self.__facts:
            if fact.get_concept().get_name() == concept_name:
                facts.append(fact)
        
        return facts
