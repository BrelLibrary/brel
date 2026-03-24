"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

===================="""

from typing import Optional

from lxml.etree import parse
from brel.contexts.filing_context import FilingContext
from brel.parsers.XML.xml_parse_catalog import parse_catalog_xml

CATALOG_FILEPATH = "META-INF/catalog.xml"


def get_catalog_filepath(filepaths: list[str]) -> Optional[str]:
    """
    Get the catalog tree.
    """
    catalog_filepaths = [
        filepath for filepath in filepaths if filepath.endswith(CATALOG_FILEPATH)
    ]

    if not catalog_filepaths:
        return None

    # Longer names mean deeper into the directory substructure, and we want it to be at surface-level
    catalog_filepaths.sort(key=lambda name: len(name))
    return catalog_filepaths[0]


def parse_catalog(filepaths: list[str], context: FilingContext) -> None:
    """
    Parse the catalog.
    """
    catalog_filepath = get_catalog_filepath(filepaths)

    if not catalog_filepath:
        return

    filepaths.remove(catalog_filepath)
    catalog_tree = parse(catalog_filepath)
    parse_catalog_xml(catalog_filepath, catalog_tree, context)


def create_filing_context(entrypoint_filepaths: list[str]) -> FilingContext:
    context = FilingContext()
    parse_catalog(entrypoint_filepaths, context)

    xml_service = context.get_xml_service()
    for filepath in entrypoint_filepaths:
        xml_service.add_etree_recursive(filepath)
    return context
