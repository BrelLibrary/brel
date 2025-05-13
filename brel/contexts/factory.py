"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

===================="""

from brel.contexts.filing_context import FilingContext


def create_filing_context(
    entrypoint_filepaths: list[str],
) -> FilingContext:
    context = FilingContext()
    xml_service = context.get_xml_service()
    for filepath in entrypoint_filepaths:
        xml_service.add_etree_recursive(filepath)
    return context
