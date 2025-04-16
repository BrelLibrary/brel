from brel.parsers.dts.factory import create_xml_repository
from brel.parsers.xml_filing_parser import XMLFilingParser
from brel.parsers.xhtml_filing_parser import XHTMLFilingParser
from brel.contexts.filing_context import FilingContext


def create_xml_filing_parser(
    context: FilingContext, entrypoint_filepaths: list[str]
) -> XMLFilingParser:
    xml_repository = create_xml_repository(entrypoint_filepaths)
    return XMLFilingParser(xml_repository=xml_repository, context=context)


def create_xhtml_filing_parser(entrypoint_filepaths: list[str]) -> XHTMLFilingParser:
    xml_repository = create_xml_repository(entrypoint_filepaths)
    return XHTMLFilingParser(xml_repository=xml_repository)
