from typing import Callable


class ParserResolver:
    def __init__(self, xml_parser: Callable, xhtml_parser: Callable):
        self._parsers = {".xml": xml_parser, ".xsd": xml_parser, ".xhtml": xhtml_parser}

    def get_parser(self, file_name: str):
        for ext, parser in self._parsers.items():
            if file_name.endswith(ext):
                return parser
        raise ValueError(f"No parser registered for: {file_name}")
