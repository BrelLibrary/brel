"""
This module contains the XHTMLFilingParser class.
It is responsible for taking a list of filepaths to XBRL files and parsing them using XHTML into a brel filing.

====================

- author: Shrey Mittal
- version: 0.1
- date: 30 May 2024

====================
"""

from collections.abc import Mapping
import os
from typing import Any, Iterable, Tuple

import lxml
from lxml import etree

from brel.brel_component import Component
from brel.brel_fact import Fact
from brel.networks.i_network import INetwork
from brel.parsers.XHMTL.xhtml_parse_facts import parse_facts_xhtml
from brel.parsers.XML.networks.xml_networks_parser import parse_networks_from_xmls
from brel.parsers.XML.xml_component_parser import parse_components_xml
from brel.parsers.XML.xml_namespace_normalizer import normalize_nsmap
from brel.parsers.XML.xml_report_element_parser import parse_report_elements_xml
from brel.parsers.XML.xml_sanity_checks import (
    check_duplicate_arcs,
    check_duplicate_rolerefs,
)
from brel.parsers.dts.xhtml_file_manager import XHTMLFileManager
from brel.parsers.dts.xml_file_manager import XMLFileManager
from brel.parsers.i_filing_parser import IFilingParser
from brel.parsers.utils.lxml_utils import get_all_nsmaps
from brel.qname import QName, QNameNSMap
from brel.reportelements.i_report_element import IReportElement

DEBUG = False


class XHTMLFilingParser(IFilingParser):
    def __init__(
        self,
        filepaths: list[str],
    ) -> None:
        if len(filepaths) < 1:
            raise ValueError("No filepaths provided. Make sure to provide at least one filepath.")

        self.__filing_type = "XHTML"
        self.__parser = etree.XMLParser()
        self.__print_prefix = f"{'[XHTMLFilingParser]':<20}"

        # mapping from xhtml and xml ids to report elements, facts, and components
        # handy for resolving hrefs
        self.__id_to_any: dict[str, Any] = {}

        # Make cache_path work for windows, mac and linux
        # also make it hidden
        cache_path = os.path.join(os.path.expanduser("~"), ".brel", "dts_cache")

        # load the DTS
        if DEBUG:  # pragma: no cover
            self.__print("Resolving DTS...")
        self.__file_manager = XHTMLFileManager(cache_path, filepaths, self.__parser)

        # normalize and bootstrap the QName nsmap
        if DEBUG:  # pragma: no cover
            self.__print("Normalizing nsmap...")
        self.__nsmap = self.__create_nsmap()

        check_duplicate_rolerefs(self.__file_manager, self.__nsmap)
        check_duplicate_arcs(self.__file_manager, self.__nsmap)

        if DEBUG:  # pragma: no cover
            self.__print("XMLFilingParser initialized!")
            print("-" * 50)

    def __create_nsmap(self) -> QNameNSMap:
        xml_trees = self.__file_manager.get_all_files()

        nsmaps = get_all_nsmaps(xml_trees)
        # add xml namespace to a random nsmap
        nsmaps[0]["html"] = "http://www.w3.org/1999/xhtml"
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
        for rename_uri, rename_prefixes in renames.items():
            new_prefix = rename_prefixes
            if DEBUG:
                print(f"> {rename_uri} -> {new_prefix}")
            qname_nsmap.rename(rename_uri, new_prefix)

        if DEBUG:  # pragma: no cover
            print("Note: Prefix redirects are not recommended.")

        return qname_nsmap

    def __print(self, output: str):
        """
        Print a message with the prefix [XHTMLFilingParser].
        :param output: The message to print.
        """
        if DEBUG:  # pragma: no cover
            print(self.__print_prefix, output)

    def get_nsmap(self) -> QNameNSMap:
        return self.__nsmap

    def parse_report_elements(
        self,
    ) -> Tuple[Mapping[QName, IReportElement], Iterable[Exception]]:
        """
        Parse the report elements. Even those that are not part of any network or fact.
        :returns:
        - A lookup that, given a QName, returns the report element with that QName.
        - A list of errors that occurred during parsing.
        """
        errors: list[Exception] = []

        xsd_filenames = [filename for filename in self.__file_manager.get_file_names() if filename.endswith(".xsd")]
        xsd_etrees = [self.__file_manager.get_file(filename) for filename in xsd_filenames]

        (
            report_elements,
            id_to_report_elem,
            report_element_errors,
        ) = parse_report_elements_xml(self.__file_manager, xsd_etrees, self.__nsmap)

        errors.extend(report_element_errors)

        for id, report_elem in id_to_report_elem.items():
            if id in self.__id_to_any.keys():
                errors.append(
                    ValueError(f"the id {id} is not unique. It is used by {self.__id_to_any[id]} and {report_elem}")
                )

            self.__id_to_any[id] = report_elem

        return report_elements, errors

    def parse_facts(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Tuple[Iterable[Fact], Iterable[Exception]]:
        """
        Parse the facts.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns
        - Iterable[Fact]: A list of facts.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        errors: list[Exception] = []
        all_filenames = self.__file_manager.get_file_names()
        xhtml_filenames = list(
            filter(
                lambda filename: filename.endswith(".htm") or filename.endswith("html"),
                all_filenames,
            )
        )
        xml_etrees = [self.__file_manager.get_file(filename) for filename in xhtml_filenames]

        facts, id_to_fact, facts_errors = parse_facts_xhtml(xml_etrees, report_elements, self.__nsmap)
        errors.extend(facts_errors)

        for id, fact in id_to_fact.items():
            if id in self.__id_to_any.keys():
                errors.append(ValueError(f"the id {id} is not unique. It is used by {self.__id_to_any[id]} and {fact}"))

            self.__id_to_any[id] = fact

        return facts, errors

    def parse_networks(
        self, report_elements: Mapping[QName, IReportElement]
    ) -> Tuple[Mapping[str, Iterable[INetwork]], Iterable[Exception]]:
        """
        Parse the networks and updates the report element lookup function accordingly.
        :param report_elements: A lookup function that, given a QName, returns the associated report element.
        :returns:
        - Mapping[str, Iterable[INetwork]]: A lookup function that, given a role uri, returns a list of networks with that uri.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        return parse_networks_from_xmls(
            self.__file_manager.get_all_files(),
            self.__nsmap,
            self.__id_to_any,
            report_elements,
        )

    def parse_components(
        self,
        networks: Mapping[str, Iterable[INetwork]],
    ) -> Tuple[Iterable[Component], Iterable[Exception]]:
        """
        Parse the components.
        :param networks: A lookup function that, given a role uri, returns a list of networks with that uri.
        :returns:
        - Iterable[Component]: A list of components.
        - Iterable[Exception]: A list of errors that occurred during parsing.
        """
        return parse_components_xml(
            self.__file_manager.get_all_files(),
            networks,
            self.__nsmap,
        )

    def get_filing_type(self) -> str:
        return self.__filing_type
