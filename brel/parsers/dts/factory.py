import os.path
import lxml
import lxml.etree
import lxml.html.html5parser
from functools import cache
from requests import Session
from brel.parsers.dts.file_repository import FileRepository
from brel.parsers.dts.xml_repository import XMLRepository
from brel.parsers.dts.parser_resolver import ParserResolver


def get_file_repository(entrypoint_filepaths: list[str]) -> FileRepository:
    session = Session()
    cache_location = os.path.join(os.path.expanduser("~"), ".brel", "dts_cache")
    clear_cache = False
    return FileRepository(session, cache_location, entrypoint_filepaths, clear_cache)


@cache
def get_parser_resolver() -> ParserResolver:
    return ParserResolver(
        lambda file: lxml.etree.parse(file),
        lambda file: lxml.html.html5parser.parse(file),
    )


def get_xml_repository(entrypoint_filepaths: list[str]) -> XMLRepository:
    file_repository = get_file_repository(entrypoint_filepaths)
    parser_resolver = get_parser_resolver()
    return XMLRepository(file_repository=file_repository, parser_resolver=parser_resolver)
