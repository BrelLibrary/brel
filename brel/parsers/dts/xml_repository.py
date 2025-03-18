"""
This module contains the XMLSchemaManager class.
The XMLSchemaManager class is responsible for downloading and caching XBRL taxonomies.

=================

- author: Robin Schmidiger
- version: 0.8
- date: 06 March 2025

=================
"""

import lxml
import lxml.etree
import lxml.html.html5parser
from brel.parsers.dts.file_repository import FileRepository
from brel.parsers.dts.i_file_manager import IFileManager
from brel.parsers.utils.lxml_xpath_utils import add_xpath_functions

class XMLRepository(IFileManager):
    def __init__(
        self,
        cache_location: str,
        filenames: list[str],
    ) -> None:
        self.__file_repository = FileRepository(cache_location, filenames)
        self.__xml_etree_cache: dict[str, lxml.etree._ElementTree] = {}
        self.__parsers = {
            "xml": lambda file: lxml.etree.parse(file),
            "html": lambda file: lxml.html.html5parser.parse(file)
        }
        add_xpath_functions()
    
    def get_format_type(self) -> type:
        return lxml.etree._ElementTree
    
    def get_file(self, uri: str) -> lxml.etree:
        """
        Retrieves an XML file and parses it into an lxml.etree object.

        If the file has been previously retrieved and cached, it returns the cached version.
        Otherwise, it fetches the file from the file repository, parses it, caches it, and then returns it.

        Args:
            uri (str): The URI of the XML file to retrieve.

        Returns:
            lxml.etree: The parsed XML file as an lxml.etree object.
        """
        if uri in self.__xml_etree_cache:
            return self.__xml_etree_cache[uri]
        else:
            with self.__file_repository.get_file(uri) as file:
                filetype = uri.split(".")[-1]
                parser = self.__parsers.get(filetype, self.__parsers["xml"])

                xml_etree = parser(file)
                self.__xml_etree_cache[uri] = xml_etree
                
                return xml_etree
    
    def get_all_files(self) -> list[lxml.etree._ElementTree]:
        """
        Retrieve all XML files from the file repository.

        Returns:
            list[lxml.etree._ElementTree]: A list of parsed XML files as lxml ElementTree objects.
        """
        return [self.get_file(uri) for uri in self.__file_repository.get_uris()]
        
    
    def get_file_names(self) -> list[str]:
        """
        Retrieves a list of file names from the file repository.

        Returns:
            list[str]: A list of file names (URIs) stored in the file repository.
        """
        return list(self.__file_repository.get_uris())