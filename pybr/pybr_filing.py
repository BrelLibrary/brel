import os
from typing import cast

from pybr import PyBRFact, PyBRFilingFilter, PyBRComponent, QName
from pybr.characteristics import PyBRAspect
from pybr.reportelements import IReportElement, PyBRAbstract, PyBRConcept, PyBRDimension, PyBRHypercube, PyBRLineItems, PyBRMember
from pybr.networks import INetwork
from pybr.parsers import IFilingParser, XMLFilingParser

class PyBRFiling:
    """A wrapper class for loading and manipulating a filing"""
    # TODO: update docstrings
    
    def __init__(self, parser: IFilingParser) -> None:
        parser_result = parser.parse()

        self.__networks: list[INetwork] = parser_result["networks"]
        self.__facts: list[PyBRFact] = parser_result["facts"]
        self.__reportelems: list[IReportElement] = parser_result["report elements"]
        self.__components = parser_result["components"]
    
    # first class citizens
    def get_all_pyhsical_networks(self) -> list[INetwork]:
        """
        Get all physical networks in the filing
        """
        return self.__networks
    
    def get_all_facts(self) -> list[PyBRFact]:
        """
        Get all facts in the filing
        """
        return self.__facts
    
    def get_all_report_elements(self) -> list[IReportElement]:
        """
        Get all report elements in the filing
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
    def get_all_concepts(self) -> list[PyBRConcept]:
        """
        Get all Concepts in the filing
        """
        return cast(list[PyBRConcept], list(filter(lambda x: isinstance(x, PyBRConcept), self.__reportelems)))
    
    # TODO: implement
    def get_all_abstracts(self) -> list[PyBRAbstract]:
        """
        Get all Abstracts in the filing
        """
        return cast(list[PyBRAbstract], list(filter(lambda x: isinstance(x, PyBRAbstract), self.__reportelems)))
    
    def get_all_line_items(self) -> list[PyBRLineItems]:
        """
        Get all LineItems in the filing
        """
        return cast(list[PyBRLineItems], list(filter(lambda x: isinstance(x, PyBRLineItems), self.__reportelems)))
    
    def get_all_hypercubes(self) -> list[PyBRHypercube]:
        """
        Get all Hypercubes in the filing
        """
        return cast(list[PyBRHypercube], list(filter(lambda x: isinstance(x, PyBRHypercube), self.__reportelems)))
        
    def get_all_dimensions(self) -> list[PyBRDimension]:
       """
        Get all Dimensions in the filing
        """
       return cast(list[PyBRDimension], list(filter(lambda x: isinstance(x, PyBRDimension), self.__reportelems)))
        
    def get_all_members(self) -> list[PyBRMember]:
       """
        Get all Member in the filing
        """
       return cast(list[PyBRMember], list(filter(lambda x: isinstance(x, PyBRMember), self.__reportelems)))
    
    def get_report_element_by_name(self, concept_name: QName) -> IReportElement:
        """Get a concept by its name"""
        name_matches = lambda x: x.get_name() == concept_name

        re: IReportElement = filter(name_matches, self.__reportelems).__next__()
        
        if re is None:
            raise ValueError(f"Concept {concept_name} not found")
        
        return re
    
    def get_all_reported_concepts(self) -> list[PyBRConcept]:
        """Get all concepts that are reported in the filing"""
        reported_concepts = []
        for fact in self.__facts:
            concept = fact.get_concept().get_value()
            if concept not in reported_concepts:
                reported_concepts.append(concept)
        
        return reported_concepts
    
    def get_facts_by_concept_name(self, concept_name: QName) -> list[PyBRFact]:
        """Get all facts that are associated with a concept"""
        filtered_facts = []
        for fact in self.__facts:
            concept = fact.get_concept().get_value()

            if concept.get_name() == concept_name:
                filtered_facts.append(fact)
        
        return filtered_facts
    
    def get_facts_by_concept(self, concept: PyBRConcept) -> list[PyBRFact]:
        """Get all facts that are associated with a concept"""
        return self.get_facts_by_concept_name(concept.get_name())
    
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
