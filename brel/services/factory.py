"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 2 May 2025

====================
"""

from lxml.etree import parse as parse_xml
from lxml.html import html5parser
from requests import Session
from brel.data.errors.error_repository import ErrorRepository
from brel.data.file.file_repository import FileRepository
from brel.data.namespace.namespace_repository import NamespaceRepository
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.data.uri_rewrite.uri_rewrite_repository import URIRewriteRepository
from brel.data.xml.xml_repository import XMLRepository
from brel.services.file.file_service import FileService
from brel.services.report_element.report_element_service import ReportElementService
from brel.services.xml.xml_file_parser_resolver import XMLFileParserResolver
from brel.services.xml.xml_service import XMLService


def create_report_element_service(
    report_element_repository: ReportElementRepository,
    namespace_repository: NamespaceRepository,
) -> ReportElementService:
    return ReportElementService(namespace_repository, report_element_repository)


def create_file_service(
    file_repository: FileRepository,
    error_repository: ErrorRepository,
) -> FileService:
    session = Session()
    return FileService(file_repository, error_repository, session)


def create_xml_service(
    file_service: FileService,
    xml_repository: XMLRepository,
    uri_rewrite_repository: URIRewriteRepository,
) -> XMLService:
    parser_resolver = create_xml_file_parser_resolver()
    return XMLService(
        file_service, xml_repository, uri_rewrite_repository, parser_resolver
    )


def create_xml_file_parser_resolver() -> XMLFileParserResolver:
    return XMLFileParserResolver(
        lambda content: parse_xml(content),
        lambda content: parse_xml(content),
    )
