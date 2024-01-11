"""
This module contains the XMLFilingParser class.
It is responsible for taking a list of filepaths to XBRL files and parsing them into a brel filing.

====================

- author: Robin Schmidiger
- version: 0.7
- date: 18 December 2023

====================
"""

import os
import lxml
import lxml.etree

from brel.reportelements import IReportElement
from brel import QName, Fact, Component, QNameNSMap
from brel.parsers import IFilingParser
from brel.parsers.dts import XMLFileManager
from brel.networks import INetwork
from brel.parsers.utils import get_all_nsmaps

from .XML.networks.xml_networks_parser import parse_networks_from_xmls
from brel.parsers.XML import (
    parse_components_xml,
    parse_report_elements_xml,
    parse_facts_xml,
    normalize_nsmap,
)
from brel.parsers.XML import (
    check_duplicate_rolerefs,
    check_roleref_pointers,
    check_duplicate_arcs,
)

from typing import Any

DEBUG = False


class XMLFilingParser(IFilingParser):
    def __init__(
        self,
        filepaths: list[str],
    ) -> None:
        if len(filepaths) < 1:
            raise ValueError(
                "No filepaths provided. Make sure to provide at least one filepath."
            )

        self.__filing_type = "XML"
        self.__parser = lxml.etree.XMLParser()
        self.__filing_location = os.path.commonpath(filepaths)
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"

        # if the commonpath is empty, the filing location is the current folder
        if self.__filing_location == "":
            self.__filing_location = "."

        # if the filing location is a file, crop the filename
        if not os.path.isdir(self.__filing_location):
            self.__filing_location = os.path.dirname(self.__filing_location)

        # mapping from xml ids to report elements, facts, and components
        # handy for resolving hrefs
        self.__id_to_any: dict[str, Any] = {}

        # crop the filing location from all filepaths
        for i in range(len(filepaths)):
            filepaths[i] = os.path.relpath(
                filepaths[i], self.__filing_location
            )

        # load the DTS
        if DEBUG:  # pragma: no cover
            self.__print("Resolving DTS...")
        self.__file_manager = XMLFileManager(
            "dts_cache/", self.__filing_location, filepaths, self.__parser
        )

        # normalize and bootstrap the QName nsmap
        if DEBUG:  # pragma: no cover
            self.__print("Normalizing nsmap...")
        self.__nsmap = self.__create_nsmap()

        check_duplicate_rolerefs(self.__file_manager, self.__nsmap)
        check_roleref_pointers(self.__file_manager, self.__nsmap)
        check_duplicate_arcs(self.__file_manager, self.__nsmap)

        if DEBUG:  # pragma: no cover
            self.__print("XMLFilingParser initialized!")
            print("-" * 50)

    def __create_nsmap(self) -> QNameNSMap:
        xml_trees = self.__file_manager.get_all_files()

        nsmaps = get_all_nsmaps(xml_trees)
        # add xml namespace to a random nsmap
        nsmaps[0]["xml"] = "http://www.w3.org/XML/1998/namespace"

        normalizer_result = normalize_nsmap(nsmaps)
        nsmap = normalizer_result["nsmap"]
        redirects = normalizer_result["redirects"]
        renames = normalizer_result["renames"]

        qname_nsmap = QNameNSMap()

        if DEBUG:  # pragma: no cover
            print("[QName] Prefix mappings:")
        for prefix, url in nsmap.items():
            # QName.add_to_nsmap(url, prefix)
            qname_nsmap.add_to_nsmap(url, prefix)
            if DEBUG:  # pragma: no cover
                print(f"> {prefix:20} -> {url}")

        if DEBUG:  # pragma: no cover
            print("[QName] Prefix redirects:")
        for redirect_from, redirect_to in redirects.items():
            # QName.set_redirect(redirect_from, redirect_to)
            qname_nsmap.add_redirect(redirect_from, redirect_to)
            if DEBUG:  # pragma: no cover
                print(f"> {redirect_from:10} -> {redirect_to}")

        if DEBUG:  # pragma: no cover
            print("[QName] Prefix renames:")
        for rename_to, rename_from in renames.items():
            # QName.set_rename(rename_from, rename_to)
            if DEBUG:
                print(f"> {rename_from:10} -> {rename_to}")
            qname_nsmap.rename(rename_from, rename_to)

        if DEBUG:  # pragma: no cover
            print("Note: Prefix redirects are not recommended.")

        return qname_nsmap

    def __print(self, output: str):
        """
        Print a message with the prefix [XMLFilingParser].
        """
        if DEBUG:  # pragma: no cover
            print(self.__print_prefix, output)

    def get_nsmap(self) -> QNameNSMap:
        return self.__nsmap

    def parse_report_elements(self) -> dict[QName, IReportElement]:
        """
        Parse the concepts.
        @return: A list of all the concepts in the filing, even those that are not reported.
        """
        xsd_filenames = [
            filename
            for filename in self.__file_manager.get_file_names()
            if filename.endswith(".xsd")
        ]
        xsd_etrees = [
            self.__file_manager.get_file(filename)
            for filename in xsd_filenames
        ]

        report_elems, id_to_report_elem = parse_report_elements_xml(
            self.__file_manager, xsd_etrees, self.__nsmap
        )

        for id, report_elem in id_to_report_elem.items():
            if id in self.__id_to_any.keys():
                raise ValueError(
                    f"the id {id} is not unique. It is used by {self.__id_to_any[id]} and {report_elem}"
                )

            self.__id_to_any[id] = report_elem

        return report_elems

    def parse_facts(
        self, report_elements: dict[QName, IReportElement]
    ) -> list[Fact]:
        """
        Parse the facts.
        """
        all_filenames = self.__file_manager.get_file_names()
        xml_filenames = list(
            filter(lambda filename: filename.endswith(".xml"), all_filenames)
        )
        xml_etrees = [
            self.__file_manager.get_file(filename)
            for filename in xml_filenames
        ]

        facts, id_to_fact = parse_facts_xml(
            xml_etrees, report_elements, self.__nsmap
        )

        for id, fact in id_to_fact.items():
            if id in self.__id_to_any.keys():
                raise ValueError(
                    f"the id {id} is not unique. It is used by {self.__id_to_any[id]} and {fact}"
                )

            self.__id_to_any[id] = fact

        return facts

    def parse_networks(
        self, report_elements: dict[QName, IReportElement]
    ) -> dict[str | None, list[INetwork]]:
        """
        Parse the networks.
        @param report_elements: A dictionary containing ALL report elements that the networks report against.
        @return: A dictionary of all the networks in the filing.
        """
        return parse_networks_from_xmls(
            self.__file_manager.get_all_files(),
            self.__nsmap,
            self.__id_to_any,
            report_elements,
        )

    def parse_components(
        self,
        report_elements: dict[QName, IReportElement],
        networks: dict[str | None, list[INetwork]],
    ) -> tuple[list[Component], dict[QName, IReportElement]]:
        """
        Parse the components.
        @param report_elements: A dictionary containing ALL report elements that the components report against.
        @param networks: A dictionary containing ALL networks that the components report against.
        The keys are the component names, the values are lists of networks for that component.
        @return:
         - A list of all the components in the filing.
         - A dictionary of all the report elements in the filing. These might have been altered by the components.
        """
        return parse_components_xml(
            self.__file_manager.get_all_files(),
            networks,
            report_elements,
            self.__nsmap,
        )

    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return self.__filing_type
