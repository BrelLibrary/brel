import os
import lxml
import lxml.etree
from lxml.etree import _Element as lxmlElement
from pybr import PyBRFact, PyBRConceptCharacteristic, PyBRContext, PyBRAspect, PyBRFilingFilter, PyBRComponent
from pybr import QName
from pybr.PyBRLinkbase import PyBRLinkbase
from pybr.parsers import IFilingParser, XMLFilingParser

class PyBRFiling:
    """A wrapper class for loading and manipulating a filing"""

    """
    The methods of this class are the following:
    - 1st class methods
    --> static open(FilePath | URL file_path): PyBRFiling
    --> get_all_facts(): list[PyBRFact]
    --> get_all_concepts(): list[PyBRConcept]
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
        self.__reportelems = parser_result["report elements"]
        self.__components = parser_result["components"]
    
    # first class citizens
    def get_all_facts(self) -> list[PyBRFact]:
        """
        Get all facts in the filing
        """
        return self.__facts
    
    def get_all_concepts(self) -> list[PyBRConceptCharacteristic]:
        """
        Get all concepts in the filing
        """
        return self.__reportelems
    
    def get_all_components(self) -> list[PyBRComponent]:
        """
        Get all components in the filing
        """
        return self.__components
    
    @classmethod
    def open(cls, folder_path):
        """Load a filing from a local folder"""
        # check if the folder path is a string ending with a slash
        if not isinstance(folder_path, str) or not folder_path.endswith("/"):
            raise ValueError(f"The path {folder_path} is not a valid folder path. It has to end with a slash '/'")

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
    
    # second class citizens
    def get_concept_by_name(self, concept_name: QName) -> PyBRConceptCharacteristic:
        """Get a concept by its name"""
        concept: PyBRConceptCharacteristic | None = None
        for c in self.__reportelems:
            if c.get_value() == concept_name:
                concept = c
                break
        
        if concept is None:
            raise ValueError(f"Concept {concept_name} not found")
        
        return concept
    
    def get_all_reported_concepts(self) -> list[PyBRConceptCharacteristic]:
        """Get all concepts that are reported in the filing"""
        reported_concepts = []
        for fact in self.__facts:
            if fact.get_concept() not in reported_concepts:
                reported_concepts.append(fact.get_concept())
        
        return reported_concepts
    
    def get_facts_by_concept_name(self, concept_name: QName) -> list[PyBRFact]:
        """Get all facts that are associated with a concept"""
        filtered_facts = []
        for fact in self.__facts:
            concept = fact.get_concept()

            if concept.get_value() == concept_name:
                filtered_facts.append(fact)
        
        return filtered_facts
    
    def get_facts_by_concept(self, concept: PyBRConceptCharacteristic) -> list[PyBRFact]:
        """Get all facts that are associated with a concept"""
        return self.get_facts_by_concept_name(concept.get_value())
    
    def __getitem__(self, key: str | QName | PyBRAspect | PyBRFilingFilter | bool) -> list[PyBRFact] | PyBRFilingFilter:
        # TODO: make this typecheck

        # if the key is a filter, filter the facts
        if isinstance(key, PyBRFilingFilter):
            return key.filter(self.__facts)
        
        # if the key is an aspect, make a filter of that aspect and return the unappied filter
        if isinstance(key, PyBRAspect):
            return PyBRFilingFilter.make_aspect_filter(self.__facts, key)
        
        # if the key is a str, but looks like a QName, then turn it into a QName
        if isinstance(key, str) and QName.is_str_qname(key):
            key = QName.from_string(key)
        
        # if the key is a qname, then it is an additional dimension
        # make a filter of that aspect and return it unapplied
        if isinstance(key, QName):
            aspect = PyBRAspect.from_QName(key)
            return PyBRFilingFilter.make_aspect_filter(self.__facts, aspect)
        
        # finally, if the key is one of the core aspects, then make a filter of that aspect and return it unapplied
        # TODO: add custom aspects as well
        aspect_names = {
            "entity": PyBRAspect.ENTITY, 
            "period": PyBRAspect.PERIOD, 
            "unit": PyBRAspect.UNIT, 
            "concept": PyBRAspect.CONCEPT
             }
        
        if key in aspect_names:
            key = aspect_names[key]
            return PyBRFilingFilter.make_aspect_filter(self.__facts, key)
        
        # otherwise, raise an error
        raise ValueError(f"Key {key} is not a valid key")
