"""
This module contains the XMLSchemaManager class.
The XMLSchemaManager class is responsible for downloading and caching XBRL taxonomies.

@author: Robin Schmidiger
@version: 0.0.5
@date: 18 December 2023
"""

DEBUG = True

import os
from typing import Any
import lxml
import lxml.etree
import requests
from io import BytesIO

from brel.parsers.dts import IFileManager
from brel import QName

from collections import defaultdict

class XMLFileManager(IFileManager):
    """
    Class for downloading and caching XBRL files in the XML format.
    """

    def __init__(self, cache_location: str, filing_location: str, filenames: list[str], parser: lxml.etree.XMLParser) -> None:
        # check if all the paths are valid
        if not os.path.isdir(cache_location):
            raise ValueError(f"{cache_location} is not a valid folder path")
        
        if not os.path.isdir(filing_location):
            raise ValueError(f"{filing_location} is not a valid folder path")
        
        # check if all the schema filenames are in the filing location
        for filename in filenames:
            if filename not in os.listdir(filing_location):
                raise ValueError(f"{filename} is not a file in the folder {filing_location}")
        
        # set class variables
        self.__parser = parser

        self.__filing_location = filing_location
        self.cache_location = cache_location

        self.__filenames: list[str] = []
        self.__file_cache: dict[str, lxml.etree._ElementTree] = {}
        self.__file_prefixes: dict[str, list[str]] = defaultdict(list)

        # populate the cache
        for filename in filenames:
            self.__load_dts(self.__filing_location + filename)

        if DEBUG:  # pragma: no cover
            print(f"filenames: {self.__filenames}")

    def uri_to_filename(self, url: str) -> str:
        """
        Convert a url to a filename.
        @param url: The url to convert.
        @return: The filename.
        """
        prefix = QName.get_prefix_from_url(url)
        version = QName.get_version_from_url(url)

        if url.endswith(".xsd"):
            file_format = "xsd"
        elif url.endswith(".xml"):
            file_format = "xml"
        else:
            raise ValueError(f"url: {url} is not a valid schema url. It must end with .xsd or .xml")

        if version is not None:
            filename = f"{prefix}_{version}.{file_format}"
        else:
            filename = f"{prefix}.{file_format}"

        return filename
    
    def get_schema(self, schema_uri: str) -> lxml.etree._ElementTree:
        """
        Load a schema, potentially from the cache.
        @param schema_filename: The filename of the schema.
        @return: The schema as an lxml.etree._ElementTree.
        """
        
        schema_filename = self.uri_to_filename(schema_uri)

        if  schema_filename not in self.__filenames:
            raise ValueError(f"The schema {schema_filename} is not in the dts")

        # check schema cache
        if schema_filename in self.__file_cache:
            schema_xml = self.__file_cache[schema_filename]
        else:
            schema_xml = lxml.etree.parse(self.cache_location + schema_filename, self.__parser)
            self.__file_cache[schema_filename] = schema_xml
        
        return schema_xml
    
    def get_all_schemas(self) -> list[lxml.etree._ElementTree]:
        """
        Returns all the schemas in the dts
        @return: A list of lxml.etree._ElementTree representing all the schemas in the dts
        """
        return [self.get_schema(schema_name) for schema_name in self.__filenames]
    
    def get_schema_names(self) -> list[str]:
        """
        Returns all the schema names in the dts
        @return: A list of str containing the schema names in the dts
        """
        return self.__filenames   

    def __download_and_store(self, uri: str, file_name: str) -> bytes:
        """
        Download a schema and store it in the cache. Returns the downloaded content as a string.
        @param uri: The uri of the schema to download.
        @param file_name: The name of the file to store the schema in.
        @return: The downloaded content as a string.
        """
        try:
            response = requests.get(uri)
        except ConnectionError:
            raise Exception(f"Could not connect to {uri}. Are you connected to the internet?")
        xsd_content = response.content

        # write the schema to the cache
        with open(self.cache_location + file_name, "wb") as f:
            f.write(xsd_content) 
        
        return xsd_content

    def __load_dts(self, uri, referencing_schema_url: str=".", loaded_under_prefix: str=""):
        """
        Download a schema and all of its dependencies
        Stores them in the cache and adds them to the list of filenames
        Note: the referencing_schema_url is necessary to resolve relative paths
        @param uri: The uri of the schema to download. Can be a url or a local file path.
        @param referencing_schema_url: The url of the schema that is referencing the schema to download.
        @param loaded_under_prefix: The prefix under which the schema is loaded.
        """

        file_name = self.uri_to_filename(uri)

        # check if the schema is already in the cache
        # TODO: add a collision check if two unrelated schemas have the same filename
        if file_name in self.__filenames:
            return

        is_url_remote = uri.startswith("http")
        is_in_filing = os.path.isfile(uri)
        is_cached = file_name in os.listdir(self.cache_location)

        if DEBUG:  # pragma: no cover
            print(f"[File Manager] uri: {uri}, file_name: {file_name}")
            if is_cached or is_in_filing:
                print(f"[File Manager] file is local")
            else:
                print(f"[File Manager] file is remote")

        if is_cached:
            # load the schema from the cache
            with open(self.cache_location + file_name, "rb") as f:
                xsd_content: bytes = f.read()

        elif is_url_remote:
            # if the file is online, load it from the url
            xsd_content = self.__download_and_store(uri, file_name)

        elif is_in_filing:
            # otherwise load it from the current directory
            with open(uri, "rb") as f:
                xsd_content = f.read()

        else:
            # if the file is not cached, online or in the filing, then it must be in the file system of the
            # schema that is referencing it
            # so I transform the xsd_url from a local file path to a url
            uri = referencing_schema_url.rsplit("/", 1)[0] + "/" + uri
            xsd_content = self.__download_and_store(uri, file_name)
        
        # parse the schema
        xsd_tree = lxml.etree.parse(BytesIO(xsd_content), parser=self.__parser)
        # load it into the cache
        self.__file_cache[file_name] = xsd_tree
        # add it to the list of filenames
        self.__filenames.append(file_name)
        # add it to the list of prefixes
        self.__file_prefixes[file_name].append(loaded_under_prefix)

        # check all the imports in the schema
        imports = xsd_tree.findall("{http://www.w3.org/2001/XMLSchema}import")
        for xsd_import in imports:
            # for all imports, load the schema recursively
            # and add it to the current schema
            schema_location = xsd_import.attrib["schemaLocation"]
            self.__load_dts(schema_location, uri)
        