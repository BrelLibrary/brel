"""
Contains the Filing class.
This class represents an XBRL filing in the Open Information Model.

Example of how to use this class:

'''
from brel import Filing
from brel.utils import pprint_facts

# open the filing
filing = Filing.open("my_filing.zip")

# get all of the facts
facts = filing.get_all_facts()

# print the first 10 facts
pprint_facts(facts[:10])


@author: Robin Schmidiger
@version: 0.3
@date: 2023-12-19
"""

import os
import zipfile
from typing import cast, Callable, TypeGuard

from brel import Fact, FilingFilter, Component, QName
from brel.characteristics import BrelAspect
from brel.reportelements import (
    IReportElement,
    Abstract,
    Concept,
    Dimension,
    Hypercube,
    LineItems,
    Member,
)
from brel.networks import INetwork
from brel.parsers import IFilingParser, XMLFilingParser

DEBUG = True


class Filing:
    """
    Represents an XBRL filing in the Open Information Model.
    """

    def __init__(self, parser: IFilingParser) -> None:
        parser_result = parser.parse()

        self.__networks: list[INetwork] = parser_result["networks"]
        self.__facts: list[Fact] = parser_result["facts"]
        self.__reportelems: list[IReportElement] = parser_result["report elements"]
        self.__components = parser_result["components"]
        self.__nsmap = parser_result["nsmap"]

    # first class citizens
    def get_all_pyhsical_networks(self) -> list[INetwork]:
        """
        Get all physical networks in the filing
        :return: a list of all physical networks in the filing.
        """
        physical_networks = [
            network for network in self.__networks if network.is_physical()
        ]
        return physical_networks

    def get_all_facts(self) -> list[Fact]:
        """
        :return: a list of all facts in the filing.
        """
        return self.__facts

    def get_all_report_elements(self) -> list[IReportElement]:
        """
        :return: a list of all report elements in the filing.
        """
        return self.__reportelems

    def get_all_components(self) -> list[Component]:
        """
        :return: a list of all components in the filing.
        Note: components are sometimes called "roles" in the XBRL specification.
        """
        return self.__components

    @classmethod
    def open(cls, path, *args) -> "Filing":
        """
        Load a filing from a path.
        :param path: the path to the filing. This can be a folder, an xml file, or a zip file.
        :return: a Filing object with the filing loaded.
        """
        # check if the path is a folder or a file
        is_file = os.path.isfile(path)
        is_dir = os.path.isdir(path)

        if is_dir:
            if not path.endswith("/"):
                path += "/"

            folder_filenames = os.listdir(path)
            xml_files = list(filter(lambda x: x.endswith("xml"), folder_filenames))

            def prepend_path(filename: str) -> str:
                return path + filename

            xml_files = list(map(prepend_path, xml_files))

            parser = XMLFilingParser(xml_files)
            return cls(parser)
        elif is_file and path.endswith(".xml"):
            xml_files = [path]
            for arg in args:
                if os.path.isfile(arg) and arg.endswith(".xml"):
                    xml_files.append(arg)
            parser = XMLFilingParser(xml_files)
            return cls(parser)
        elif is_file and path.endswith(".zip"):
            dir_path = os.path.dirname(path)
            print(f"Extracting {path} to {dir_path} and loading it")
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(dir_path)
                # get all file paths ending in xml
                xml_files = list(
                    filter(lambda x: x.endswith("xml"), zip_ref.namelist())
                )
            print(f"Finished extracting...")

            xml_files = list(map(lambda x: dir_path + "/" + x, xml_files))
            return cls.open(*xml_files)
        else:
            raise ValueError(f"{path} is not a valid folder path")

    # second class citizens
    def get_all_concepts(self) -> list[Concept]:
        """
        :returns: a list of all concepts in the filing.
        Note that concepts are defined according to the Open Information Model. They are not the same as abstracts, line items, hypercubes, dimensions, or members.
        """
        return cast(
            list[Concept],
            list(filter(lambda x: isinstance(x, Concept), self.__reportelems)),
        )

    def get_all_abstracts(self) -> list[Abstract]:
        """
        :returns: a list of all abstracts in the filing.
        """
        return cast(
            list[Abstract],
            list(filter(lambda x: isinstance(x, Abstract), self.__reportelems)),
        )

    def get_all_line_items(self) -> list[LineItems]:
        """
        :returns: a list of all line items in the filing.
        """
        return cast(
            list[LineItems],
            list(filter(lambda x: isinstance(x, LineItems), self.__reportelems)),
        )

    def get_all_hypercubes(self) -> list[Hypercube]:
        """
        :returns: a list of all hypercubes in the filing.
        """
        return cast(
            list[Hypercube],
            list(filter(lambda x: isinstance(x, Hypercube), self.__reportelems)),
        )

    def get_all_dimensions(self) -> list[Dimension]:
        """
        :returns: a list of all dimensions in the filing.
        """
        return cast(
            list[Dimension],
            list(filter(lambda x: isinstance(x, Dimension), self.__reportelems)),
        )

    def get_all_members(self) -> list[Member]:
        """
        :returns: a list of all members in the filing.
        """
        return cast(
            list[Member],
            list(filter(lambda x: isinstance(x, Member), self.__reportelems)),
        )

    def get_report_element_by_name(
        self, element_qname: QName | str
    ) -> IReportElement | None:
        """
        :param element_qname: the name of the report element to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns: the report element with the given name. If no report element is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(element_qname, str):
            element_qname = QName.from_string(element_qname, self.__nsmap)

        name_matches = lambda x: x.get_name() == element_qname

        re: IReportElement | None = next(filter(name_matches, self.__reportelems), None)

        return re

    def get_concept_by_name(self, concept_qname: QName | str) -> Concept | None:
        """
        :param concept_qname: the name of the concept to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns: the concept with the given name. If no concept is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(concept_qname, str):
            concept_qname = QName.from_string(concept_qname, self.__nsmap)

        def concept_matches(x: IReportElement) -> TypeGuard[Concept]:
            return isinstance(x, Concept) and x.get_name() == concept_qname

        concept: Concept | None = next(
            filter(concept_matches, self.__reportelems), None
        )

        return concept

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

    def __getitem__(
        self, key: str | QName | BrelAspect | FilingFilter
    ) -> list[Fact] | FilingFilter:
        # if the key is a filter, filter the facts
        if isinstance(key, FilingFilter):
            return key.filter(self.__facts)

        # if the key is an aspect, make a filter of that aspect and return the unappied filter
        if isinstance(key, BrelAspect):
            return FilingFilter.make_aspect_filter(self.__facts, key, self.__nsmap)

        # if the key is a str, but looks like a QName, then turn it into a QName
        if isinstance(key, str) and QName.is_str_qname(key, self.__nsmap):
            key = QName.from_string(key, self.__nsmap)

        # if the key is a qname, then it is an additional dimension
        # make a filter of that aspect and return it unapplied
        if isinstance(key, QName):
            aspect = BrelAspect.from_QName(key)
            return FilingFilter.make_aspect_filter(self.__facts, aspect, self.__nsmap)

        # finally, if the key is one of the core aspects, then make a filter of that aspect and return it unapplied
        aspect_names = {
            "entity": BrelAspect.ENTITY,
            "period": BrelAspect.PERIOD,
            "unit": BrelAspect.UNIT,
            "concept": BrelAspect.CONCEPT,
        }

        if key.lower() in aspect_names:
            key = aspect_names[key]
            return FilingFilter.make_aspect_filter(self.__facts, key, self.__nsmap)

        # otherwise, raise an error
        raise ValueError(f"Key {key} is not a valid key")
