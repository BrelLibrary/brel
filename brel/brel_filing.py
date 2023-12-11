import os
from typing import cast

from brel import Fact, FilingFilter, Component, QName
from brel.characteristics import BrelAspect
from brel.reportelements import IReportElement, Abstract, Concept, Dimension, Hypercube, LineItems, Member
from brel.networks import INetwork
from brel.parsers import IFilingParser, XMLFilingParser

class Filing:
    """A wrapper class for loading and manipulating a filing"""
    
    def __init__(self, parser: IFilingParser) -> None:
        parser_result = parser.parse()

        self.__networks: list[INetwork] = parser_result["networks"]
        self.__facts: list[Fact] = parser_result["facts"]
        self.__reportelems: list[IReportElement] = parser_result["report elements"]
        self.__components = parser_result["components"]
    
    # first class citizens
    def get_all_pyhsical_networks(self) -> list[INetwork]:
        """
        Get all physical networks in the filing
        """
        physical_networks = [network for network in self.__networks if network.is_physical()]
        return physical_networks
    
    def get_all_facts(self) -> list[Fact]:
        """
        Get all facts in the filing
        """
        return self.__facts
    
    def get_all_report_elements(self) -> list[IReportElement]:
        """
        Get all report elements in the filing
        """
        return self.__reportelems
    
    def get_all_components(self) -> list[Component]:
        """
        Get all components in the filing
        """
        return self.__components
    
    @classmethod
    def open(cls, path, **kwargs):
        """Load a filing from a local folder"""
        
        if path.endswith("/"):
            if not os.path.isdir(path):
                raise ValueError(f"{path} is not a valid folder path")

            folder_filenames = os.listdir(path)
            instance_file = next(filter(lambda x: x.endswith("htm.xml"), folder_filenames))
            networks: list[str] = list(filter(lambda x: x.endswith("xml") and not x.endswith("htm.xml"), folder_filenames))

            def prepend_path(filename: str) -> str:
                return path + filename
            
            networks = list(map(prepend_path, networks))
            instance_file = prepend_path(instance_file)

            parser = XMLFilingParser(instance_file, networks)
            return cls(parser)
        elif path.endswith(".xml"):
            instance_file = path
            networks = kwargs.get("linkbases", [])
            parser = XMLFilingParser(instance_file, networks)
            return cls(parser)
        else:
            raise ValueError(f"{path} is not a valid folder path")

    
    # second class citizens
    def get_all_concepts(self) -> list[Concept]:
        """
        Get all Concepts in the filing
        """
        return cast(list[Concept], list(filter(lambda x: isinstance(x, Concept), self.__reportelems)))
    
    # TODO: implement
    def get_all_abstracts(self) -> list[Abstract]:
        """
        Get all Abstracts in the filing
        """
        return cast(list[Abstract], list(filter(lambda x: isinstance(x, Abstract), self.__reportelems)))
    
    def get_all_line_items(self) -> list[LineItems]:
        """
        Get all LineItems in the filing
        """
        return cast(list[LineItems], list(filter(lambda x: isinstance(x, LineItems), self.__reportelems)))
    
    def get_all_hypercubes(self) -> list[Hypercube]:
        """
        Get all Hypercubes in the filing
        """
        return cast(list[Hypercube], list(filter(lambda x: isinstance(x, Hypercube), self.__reportelems)))
        
    def get_all_dimensions(self) -> list[Dimension]:
       """
        Get all Dimensions in the filing
        """
       return cast(list[Dimension], list(filter(lambda x: isinstance(x, Dimension), self.__reportelems)))
        
    def get_all_members(self) -> list[Member]:
       """
        Get all Member in the filing
        """
       return cast(list[Member], list(filter(lambda x: isinstance(x, Member), self.__reportelems)))
    
    def get_report_element_by_name(self, concept_name: QName) -> IReportElement:
        """Get a concept by its name"""
        name_matches = lambda x: x.get_name() == concept_name

        re: IReportElement = filter(name_matches, self.__reportelems).__next__()
        
        if re is None:
            raise ValueError(f"Concept {concept_name} not found")
        
        return re
    
    def get_all_reported_concepts(self) -> list[Concept]:
        """Get all concepts that are reported in the filing"""
        reported_concepts = []
        for fact in self.__facts:
            concept = fact.get_concept().get_value()
            if concept not in reported_concepts:
                reported_concepts.append(concept)
        
        return reported_concepts
    
    def get_facts_by_concept_name(self, concept_name: QName) -> list[Fact]:
        """Get all facts that are associated with a concept"""
        filtered_facts = []
        for fact in self.__facts:
            concept = fact.get_concept().get_value()

            if concept.get_name() == concept_name:
                filtered_facts.append(fact)
        
        return filtered_facts
    
    def get_facts_by_concept(self, concept: Concept) -> list[Fact]:
        """Get all facts that are associated with a concept"""
        return self.get_facts_by_concept_name(concept.get_name())
    
    def __getitem__(self, key: str | QName | BrelAspect | FilingFilter | bool) -> list[Fact] | FilingFilter:
        # TODO: make this typecheck

        # if the key is a filter, filter the facts
        if isinstance(key, FilingFilter):
            return key.filter(self.__facts)
        
        # if the key is an aspect, make a filter of that aspect and return the unappied filter
        if isinstance(key, BrelAspect):
            return FilingFilter.make_aspect_filter(self.__facts, key)
        
        # if the key is a str, but looks like a QName, then turn it into a QName
        if isinstance(key, str) and QName.is_str_qname(key):
            key = QName.from_string(key)
        
        # if the key is a qname, then it is an additional dimension
        # make a filter of that aspect and return it unapplied
        if isinstance(key, QName):
            aspect = BrelAspect.from_QName(key)
            return FilingFilter.make_aspect_filter(self.__facts, aspect)
        
        # finally, if the key is one of the core aspects, then make a filter of that aspect and return it unapplied
        # TODO: add custom aspects as well
        aspect_names = {
            "entity": BrelAspect.ENTITY, 
            "period": BrelAspect.PERIOD, 
            "unit": BrelAspect.UNIT, 
            "concept": BrelAspect.CONCEPT
             }
        
        if key in aspect_names:
            key = aspect_names[key]
            return FilingFilter.make_aspect_filter(self.__facts, key)
        
        # otherwise, raise an error
        raise ValueError(f"Key {key} is not a valid key")
