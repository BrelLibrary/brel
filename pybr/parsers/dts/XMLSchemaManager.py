import os
from typing import Any
import lxml
import lxml.etree
import requests
import validators
from io import BytesIO
from pybr import QName

class XMLSchemaManager:
    """
    Class for downloading and caching XBRL taxonomies
    """

    def __init__(self, cache_location: str, filing_location: str) -> None:
        self.__cache_location = cache_location
        self.__filing_location = filing_location

        self.__parser = lxml.etree.XMLParser(
            remove_blank_text=True,
            remove_comments=True,
            remove_pis=True,
            resolve_entities=False,
            recover=True,
            huge_tree=True,
            encoding="utf-8",
        )

        self.__xbrl_schema_cache = {}

        filenames = os.listdir(filing_location)
        schema_filename = None
        for filename in filenames:
            if filename.endswith(".xsd"):
                schema_filename = filename
                break
        
        if not schema_filename:
            raise Exception("No schema found in filing")

        self.__download_dts(schema_filename)

    def __url_to_filename(self, url: str) -> str:
        """
        Convert a url to a filename.
        @param url: The url to convert.
        @return: The filename.
        """
        # TODO: This is not good enough
        return url.split("/")[-1]

        # # first strip the protocol
        # url = url.split("://")[-1]

        # # then strip the file extension
        # url = url.replace(".xsd", "")

        # # then replace all slashes with underscores
        # url = url.replace("/", "_")

        # # then replace all colons with underscores
        # url = url.replace(":", "_")

        # # then replace all dots with underscores
        # url = url.replace(".", "_")

        # # add back the file extension
        # url = url + ".xsd"

        # return url
    
    def get_schema(self, schema_uri: str) -> lxml.etree._ElementTree:
        """
        Load a schema, potentially from the cache.
        @param schema_filename: The filename of the schema.
        @return: The schema as an lxml.etree._ElementTree.
        """
        if validators.url(schema_uri):
            schema_uri = self.__url_to_filename(schema_uri)

        # check schema cache
        if schema_uri in self.__xbrl_schema_cache:
            schema_xml = self.__xbrl_schema_cache[schema_uri]
        else:
            schema_xml = lxml.etree.parse(self.__cache_location + schema_uri, self.__parser)
            self.__xbrl_schema_cache[schema_uri] = schema_xml
        
        return schema_xml

    def __download_dts(self, xsd_url, referencing_schema_url="."):
    
        """
        Download a schema and all of its dependencies
        Stores them in the cache
        """

        file_name = self.__url_to_filename(xsd_url)

        is_url_remote = xsd_url.startswith("http")
        is_in_filing = file_name in os.listdir(self.__filing_location)
        is_cached = file_name in os.listdir(self.__cache_location)

        if is_cached:
            # if the file is cached, load it from the cache
            # with open(self.__cache_location + file_name, "rb") as f:
            #     xsd_content = f.read()
            # self.print(f"> Schema {xsd_url} and dependencies already in cache")
            pass

        elif is_url_remote:
            # if the file is online, load it from the url
            response = requests.get(xsd_url)
            xsd_content = response.content

        elif is_in_filing:
            # otherwise load it from the current directory
            with open(self.__filing_location + xsd_url, "rb") as f:
                xsd_content = f.read()

        else:
            # if the file is not cached, online or in the filing, then it must be in the file system of the
            # schema that is referencing it
            # so I transform the xsd_url from a local file path to a url

            xsd_url = referencing_schema_url.rsplit("/", 1)[0] + "/" + xsd_url

            response = requests.get(xsd_url)
            xsd_content = response.content
        
        if not is_cached:
            parser = self.__parser
            xsd_tree = lxml.etree.parse(BytesIO(xsd_content), parser=parser)

            # check all the imports in the schema
            imports = xsd_tree.findall("{http://www.w3.org/2001/XMLSchema}import")
            for xsd_import in imports:
                # for all imports, load the schema recursively
                # and add it to the current schema
                schema_location = xsd_import.attrib["schemaLocation"]
                self.__download_dts(schema_location, xsd_url)
            
            # write the schema to the cache with the updated imports
            with open(self.__cache_location + file_name, "wb") as f:
                f.write(lxml.etree.tostring(xsd_tree))
            print(f"Loaded schema {xsd_url} into cache")