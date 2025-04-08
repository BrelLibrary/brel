from brel.parsers.dts.factory import get_xml_repository
from brel.parsers.xml_filing_parser import XMLFilingParser
from brel.parsers.xhtml_filing_parser import XHTMLFilingParser


def get_xml_filing_parser(entrypoint_filepaths: list[str]) -> XMLFilingParser:
    xml_repository = get_xml_repository(entrypoint_filepaths)
    return XMLFilingParser(xml_repository=xml_repository)


def get_xhtml_filing_parser(entrypoint_filepaths: list[str]) -> XMLFilingParser:
    xml_repository = get_xml_repository(entrypoint_filepaths)
    return XHTMLFilingParser(xml_repository=xml_repository)
