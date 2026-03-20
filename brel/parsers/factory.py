"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from brel.parsers.xml_filing_parser import XMLFilingParser
from brel.parsers.xhtml_filing_parser import XHTMLFilingParser
from brel.contexts.filing_context import FilingContext


def create_xml_filing_parser(context: FilingContext) -> XMLFilingParser:
    return XMLFilingParser(context)


def create_xhtml_filing_parser(context: FilingContext) -> XHTMLFilingParser:
    return XHTMLFilingParser(context)
