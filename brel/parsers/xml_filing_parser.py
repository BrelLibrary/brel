"""
This module contains the XMLFilingParser class.
It is responsible for taking a list of filepaths to XBRL files and parsing them into a brel filing.

====================

- author: Robin Schmidiger
- version: 0.10
- date: 15 April 2025

====================
"""


from brel.parsers.XML.xml_component_parser import parse_components_xml
from brel.parsers.XML.xml_facts_parser import parse_facts_xml
from brel.parsers.XML.xml_report_element_parser import parse_report_elements_xml
from brel.parsers.filing_parser import FilingParser
from brel.contexts.filing_context import FilingContext
from brel.parsers.XML.networks.xml_networks_parser import parse_networks_from_xmls
from brel.parsers.utils.lxml_utils import get_all_nsmaps


class XMLFilingParser(FilingParser):
    def __init__(
        self,
        context: FilingContext,
    ) -> None:
        super().__init__(context=context)
        self.__filing_type = "XML"
        self.__create_nsmap()

    def __create_nsmap(self) -> None:
        namespace_repository = self.get_context().get_namespace_repository()
        xml_service = self.get_context().get_xml_service()

        namespace_repository.upsert("xml", "http://www.w3.org/XML/1998/namespace")

        xml_trees = xml_service.get_all_etrees()
        for nsmap in get_all_nsmaps(xml_trees):
            for prefix, url in nsmap.items():
                namespace_repository.upsert(prefix, url)

    def parse_report_elements(self) -> None:
        parse_report_elements_xml(self.get_context())

    def parse_facts(self) -> None:
        parse_facts_xml(self.get_context())

    def parse_networks(self) -> None:
        parse_networks_from_xmls(self.get_context())

    def parse_components(self) -> None:
        parse_components_xml(self.get_context())

    def get_filing_type(self) -> str:
        return self.__filing_type
