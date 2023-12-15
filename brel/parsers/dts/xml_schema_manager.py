"""
This module contains the XMLSchemaManager class.
The XMLSchemaManager class is responsible for downloading and caching XBRL taxonomies.

@author: Robin Schmidiger
@version: 0.0.5
@date: 13 December 2023
"""

DEBUG = False

import os
from typing import Any
import lxml
import lxml.etree
import requests
import validators
from io import BytesIO

from brel.parsers.dts import IFileManager
from brel import QName

class XMLFileManager(IFileManager):
    """
    Class for downloading and caching XBRL taxonomies
    """

    def __init__(self, cache_location: str, filing_location: str, schema_filename: str, parser: lxml.etree.XMLParser) -> None:
        self.cache_location = cache_location

        if not os.path.isdir(self.cache_location):
            raise ValueError(f"{self.cache_location} is not a valid folder path")
        
        if not os.path.isdir(filing_location):
            raise ValueError(f"{filing_location} is not a valid folder path")
        
        if not schema_filename in os.listdir(filing_location):
            raise ValueError(f"{schema_filename} is not a file  the folder {filing_location}")

        self.__filing_location = filing_location
        self.__main_schema_filename = schema_filename

        # self.__parser = lxml.etree.XMLParser(
        #     remove_blank_text=True,
        #     remove_comments=True,
        #     remove_pis=True,
        #     resolve_entities=False,
        #     recover=True,
        #     huge_tree=True,
        #     encoding="utf-8",
        # )
        self.__parser = parser

        self.__xbrl_schema_cache: dict[str, lxml.etree._ElementTree] = {}

        self.__download_dts(self.__filing_location + self.__main_schema_filename)

        # iterate over all files in the cache and add them to the schema names
        # self.__schema_names = []
        # for filename in os.listdir(self.__cache_location):
        #     if filename.endswith(".xsd"):
        #         self.__schema_names.append(filename)
        self.__schema_names: list[str] = []
        self.__compute_schema_names_closure(self.__filing_location + self.__main_schema_filename)
        if DEBUG:  # pragma: no cover
            print(f"Schema names: {self.__schema_names}")

    def url_to_filename(self, url: str) -> str:
        """
        Convert a url to a filename.
        @param url: The url to convert.
        @return: The filename.
        """
        prefix = QName.get_prefix_from_url(url)
        version = QName.get_version_from_url(url)

        if version is not None:
            filename = f"{prefix}_{version}.xsd"
        else:
            filename = f"{prefix}.xsd"
        # TODO: add collisionchecker if two urls have the same filename and are not versions
        return filename
    
    def get_schema(self, schema_uri: str, populate_namelist: bool = False) -> lxml.etree._ElementTree:
        """
        Load a schema, potentially from the cache.
        @param schema_filename: The filename of the schema.
        @return: The schema as an lxml.etree._ElementTree.
        """
        
        schema_filename = self.url_to_filename(schema_uri)

        if populate_namelist and schema_filename not in self.__schema_names:
            self.__schema_names.append(schema_filename)

        if  schema_filename not in self.__schema_names:
            raise ValueError(f"The schema {schema_filename} is not in the dts")

        # check schema cache
        if schema_filename in self.__xbrl_schema_cache:
            schema_xml = self.__xbrl_schema_cache[schema_filename]
        else:
            schema_xml = lxml.etree.parse(self.cache_location + schema_filename, self.__parser)
            self.__xbrl_schema_cache[schema_filename] = schema_xml
        
        return schema_xml
    
    def get_all_schemas(self) -> list[lxml.etree._ElementTree]:
        """
        Returns all the schemas in the dts
        @return: A list of lxml.etree._ElementTree representing all the schemas in the dts
        """
        return [self.get_schema(schema_name) for schema_name in self.__schema_names]
    
    def get_schema_names(self) -> list[str]:
        """
        Returns all the schema names in the dts
        @return: A list of str containing the schema names in the dts
        """
        return self.__schema_names
        
    def __compute_schema_names_closure(self, schema_name) -> None:
        """
        Computes the closure of schema names starting from a schema name
        @param schema_name: The name of the schema to start from
        @return: A list of str containing the schema names in the dts
        """
        working_set = [schema_name]
        while len(working_set) > 0:
            schema_name = working_set.pop()
            schema = self.get_schema(schema_name, populate_namelist=True)
            imports = schema.findall("{http://www.w3.org/2001/XMLSchema}import")            

            for xsd_import in imports:
                schema_location = xsd_import.attrib["schemaLocation"]
                working_set.append(schema_location)

        # check if each namespace in the nsmap had an import statement
            

    def __download_dts(self, xsd_url, referencing_schema_url="."):
    
        """
        Download a schema and all of its dependencies
        Stores them in the cache
        """

        original_file_name = xsd_url.split("/")[-1]
        file_name = self.url_to_filename(xsd_url)

        is_url_remote = xsd_url.startswith("http")
        is_in_filing = original_file_name in os.listdir(self.__filing_location)
        is_cached = file_name in os.listdir(self.cache_location)

        if is_cached:
            # if the file is cached, load it from the cache
            # with open(self.__cache_location + file_name, "rb") as f:
            #     xsd_content = f.read()
            # self.print(f"> Schema {xsd_url} and dependencies already in cache")
            pass

        elif is_url_remote:
            # if the file is online, load it from the url
            try:
                response = requests.get(xsd_url)
            except ConnectionError:
                raise Exception(f"Could not connect to {xsd_url}. Are you connected to the internet?")
            xsd_content = response.content

        elif is_in_filing:
            # otherwise load it from the current directory
            with open(self.__filing_location + original_file_name, "rb") as f:
                xsd_content = f.read()

        else:
            # if the file is not cached, online or in the filing, then it must be in the file system of the
            # schema that is referencing it
            # so I transform the xsd_url from a local file path to a url

            xsd_url = referencing_schema_url.rsplit("/", 1)[0] + "/" + xsd_url

            try:
                response = requests.get(xsd_url)
            except ConnectionError:
                raise Exception(f"Could not connect to {xsd_url}. Are you connected to the internet?")
            xsd_content = response.content
        
        if not is_cached:
            parser = self.__parser

            # TODO: load this into the schema cache
            xsd_tree = lxml.etree.parse(BytesIO(xsd_content), parser=parser)

            # check all the imports in the schema
            # TODO: dont make this static
            imports = xsd_tree.findall("{http://www.w3.org/2001/XMLSchema}import")
            for xsd_import in imports:
                # for all imports, load the schema recursively
                # and add it to the current schema
                schema_location = xsd_import.attrib["schemaLocation"]
                self.__download_dts(schema_location, xsd_url)
            
            # write the schema to the cache with the updated imports
            with open(self.cache_location + file_name, "wb") as f:
                f.write(lxml.etree.tostring(xsd_tree))
            if DEBUG:  # pragma: no cover
                print(f"Loaded schema {xsd_url} into cache")