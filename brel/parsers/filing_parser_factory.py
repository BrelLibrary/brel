"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from brel.contexts.factory import create_filing_context
from brel.parsers.factory import create_xhtml_filing_parser, create_xml_filing_parser
from brel.parsers.filing_parser import FilingParser


class FilingParserFactory:
    def __init__(self) -> None:
        pass

    def create_parser(self, files: list[str]) -> FilingParser:
        """
        Create a filing parser based on the provided files.
        If all files are XML or XSD, an XML filing parser is created.
        If all files are XML, XSD, or HTML, an XHTML filing parser is created.
        Otherwise, a ValueError is raised.
        :param files: List of file names to determine the filing type. Cannot be empty.
        :returns: An instance of FilingParser.
        :raises ValueError: If no supported filing parser is found for the provided files.
        """
        if not files:
            raise ValueError("No files provided for parsing.")

        context = create_filing_context(files)

        # Example logic to determine the filing type based on file names
        if all(file.endswith(".xml") or file.endswith(".xsd") for file in files):
            return create_xml_filing_parser(context)
        elif all(
            file.endswith(".xml") or file.endswith(".xsd") or file.endswith(".html")
            for file in files
        ):
            return create_xhtml_filing_parser(context)
        else:
            raise ValueError(f"No supported filing parser found for files: {files}")
