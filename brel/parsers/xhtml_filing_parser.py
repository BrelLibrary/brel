"""
This module contains the XHTMLFilingParser class.
It is responsible for taking a list of filepaths to XBRL files and parsing them using XHTML into a brel filing.

====================

- author: Shrey Mittal, Robin Schmidiger
- version: 0.2
- date: 15 April 2025

====================
"""

from collections.abc import Mapping
from typing import Iterable, Tuple


from brel.brel_fact import Fact
from brel.parsers.XHMTL.xhtml_parse_facts import parse_facts_xhtml
from brel.parsers.XML.networks.xml_networks_parser import parse_networks_from_xmls
from brel.parsers.XML.xml_component_parser import parse_components_xml
from brel.parsers.XML.xml_namespace_normalizer import normalize_nsmap
from brel.parsers.XML.xml_report_element_parser import parse_report_elements_xml
from brel.parsers.dts.xml_repository import XMLRepository
from brel.parsers.filing_parser import FilingParser
from brel.parsers.utils.lxml_utils import get_all_nsmaps
from brel.qname import QName, QNameNSMap
from brel.reportelements.i_report_element import IReportElement


class XHTMLFilingParser(FilingParser):
    def __init__(
        self,
        xml_repository: XMLRepository,
    ) -> None:
        self.__filing_type = "XHTML"
        self.__xml_repository = xml_repository
        self.__nsmap = self.__create_nsmap()

    def __create_nsmap(self) -> QNameNSMap:
        xml_trees = self.__xml_repository.get_all_files()

        nsmaps = get_all_nsmaps(xml_trees)
        # add xml namespace to a random nsmap
        nsmaps[0]["html"] = "http://www.w3.org/1999/xhtml"
        nsmaps[0]["xml"] = "http://www.w3.org/XML/1998/namespace"

        normalizer_result = normalize_nsmap(nsmaps)
        nsmap = normalizer_result["nsmap"]
        redirects = normalizer_result["redirects"]
        renames = normalizer_result["renames"]

        qname_nsmap = QNameNSMap()

        for prefix, url in nsmap.items():
            # QName.add_to_nsmap(url, prefix)
            qname_nsmap.add_to_nsmap(url, prefix)

        for redirect_from, redirect_to in redirects.items():
            # QName.set_redirect(redirect_from, redirect_to)
            qname_nsmap.add_redirect(redirect_from, redirect_to)

        for rename_uri, rename_prefixes in renames.items():
            new_prefix = rename_prefixes
            qname_nsmap.rename(rename_uri, new_prefix)

        return qname_nsmap

    def parse_report_elements(self) -> None:
        xsd_filenames = [
            filename
            for filename in self.__xml_repository.get_file_names()
            if filename.endswith(".xsd")
        ]
        xsd_etrees = [
            self.__xml_repository.get_file(filename) for filename in xsd_filenames
        ]

        parse_report_elements_xml(
            context=self.get_context(),
            file_manager=self.__xml_repository,
            etrees=xsd_etrees,
        )

    def parse_facts(self) -> None:
        all_filenames = self.__xml_repository.get_file_names()
        xhtml_filenames = list(
            filter(
                lambda filename: filename.endswith(".htm") or filename.endswith("html"),
                all_filenames,
            )
        )
        xml_etrees = [
            self.__xml_repository.get_file(filename) for filename in xhtml_filenames
        ]

        parse_facts_xhtml(self.get_context(), xml_etrees)

    def parse_networks(self) -> None:
        parse_networks_from_xmls(
            self.get_context(),
            self.__xml_repository.get_all_files(),
        )

    def parse_components(self) -> None:
        parse_components_xml(
            self.get_context(),
            self.__xml_repository.get_all_files(),
        )

    def get_filing_type(self) -> str:
        return self.__filing_type
