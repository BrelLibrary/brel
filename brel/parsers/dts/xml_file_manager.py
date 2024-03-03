"""
This module contains the XMLSchemaManager class.
The XMLSchemaManager class is responsible for downloading and caching XBRL taxonomies.

=================

- author: Robin Schmidiger
- version: 0.7
- date: 29 January 2024

=================
"""

DEBUG = False

import os
import urllib
import re
from collections import defaultdict
from io import BytesIO
from typing import Any, cast

import lxml
import lxml.etree
import requests
import time

from brel.parsers.dts import IFileManager


class XMLFileManager(IFileManager):
    """
    Class for downloading and caching XBRL files in the XML format.
    """

    def __init__(
        self,
        cache_location: str,
        filenames: list[str],
        parser: lxml.etree.XMLParser,
    ) -> None:
        # check if all the paths are valid
        if not os.path.isdir(cache_location):
            # raise ValueError(f"{cache_location} is not a valid folder path")

            # create a cache folder if it does not exist
            print(f"Creating DTS cache folder at {cache_location}")
            os.makedirs(cache_location)

        # set class variables
        self.__parser = parser

        self.cache_location = cache_location

        self.__filenames: list[str] = []
        self.__file_cache: dict[str, lxml.etree._ElementTree] = {}
        self.__session = requests.Session()

        # populate the cache
        if DEBUG:  # pragma: no cover
            print("Populating DTS cache...")
        for filename in filenames:
            self.__load_dts(filename)

        if DEBUG:  # pragma: no cover
            print(f"filenames: {self.__filenames}")

    def uri_to_filename(self, uri: str) -> str:
        """
        Converts a uri to a filename.
        The filename is unique as long as the uri is unique.
        :param uri: the uri to convert
        :returns str: the filename
        """

        # the should be an absolute uri
        # the file name should be readable, but also unique
        # taking the whole uri is not a good idea, because it is too long
        # taking only the last part is not a good idea, because it is not guaranteed to be unique
        file_format = uri.split(".")[-1]
        supported_formats = ["xml", "xsd"]
        if file_format not in supported_formats:
            raise ValueError(f"File format {file_format} not supported. Supported formats are {supported_formats}.")

        if not uri.startswith("http"):
            if "/" in uri:
                return uri.split("/")[-1]
            else:
                return uri

        uri = uri.replace("." + file_format, "")

        if "http" in uri:
            # remove http and https
            uri = uri.replace("http://", "")
            uri = uri.replace("https://", "")

            # replace www. and things like .com, .org, etc.
            uri = uri.replace("www.", "")
            # the .com is between the first . and the first /
            # uri = uri.split(".")[0] + uri.split("/")[1]
        # replace all / with _
        uri = uri.replace("/", "_")
        # replace all : with _
        uri = uri.replace(":", "_")
        # replace all ? with _
        uri = uri.replace("?", "_")
        # replace all . with _
        uri = uri.replace(".", "_")
        # replace all \ with _
        uri = uri.replace("\\", "_")

        return uri + "." + file_format

    def get_file(self, schema_uri: str) -> lxml.etree._ElementTree:
        """
        Load a schema, potentially from the cache.
        :param schema_filename: The filename of the schema.
        :returns: The schema as an lxml.etree._ElementTree.
        """

        schema_filename = self.uri_to_filename(schema_uri)

        if schema_filename not in self.__filenames:
            raise ValueError(f"The schema {schema_filename} is not in the dts")

        # check schema cache
        if schema_filename in self.__file_cache:
            schema_xml = self.__file_cache[schema_filename]
        else:
            schema_xml = lxml.etree.parse(
                os.path.join(self.cache_location, schema_filename),
            )
            self.__file_cache[schema_filename] = schema_xml

        return schema_xml

    def get_all_files(self) -> list[lxml.etree._ElementTree]:
        """
        :returns: A list of lxml.etree._ElementTree representing all the schemas in the dts
        """
        return [self.get_file(schema_name) for schema_name in self.__filenames]

    def get_file_names(self) -> list[str]:
        """
        Returns all the schema names in the dts
        :returns list: All the schema names and instance names in the dts and instance files
        """
        return self.__filenames

    def __download_and_store(self, uri: str, file_name: str) -> bytes:
        """
        Download a schema and store it in the cache. Returns the downloaded content as a string.
        :param uri: The uri of the schema to download.
        :param file_name: The name of the file to store the schema in.
        :returns: The downloaded content as a string.
        """
        try:
            # TODO: make this less hacky
            # this is essentially a spoof of a user agent
            # The SEC blocks bots that are trying to scrape their data
            response = self.__session.get(uri, headers={"User-Agent": "Mozilla/5.0"})
            # sleep for 0.1 second to avoid getting blocked by the SEC
            if "sec.gov" in uri:
                time.sleep(0.1)
        except ConnectionError:
            raise Exception(f"Could not connect to {uri}. Are you connected to the internet?")

        if response.status_code != 200:
            raise Exception(f"Failed to download {uri}. The server responded with status code {response.status_code}")
        xsd_content = response.content

        # write the schema to the cache
        # with open(self.cache_location + file_name, "wb") as f:
        with open(os.path.join(self.cache_location, file_name), "wb") as f:
            f.write(xsd_content)

        return xsd_content

    def __load_dts(
        self,
        uri,
        referencing_uri: str = ".",
    ):
        """
        Download a schema and all of its dependencies
        Stores them in the cache and adds them to the list of filenames
        Note: the referencing_schema_url is necessary to resolve relative paths
        :param uri: The uri of the schema to download. Can be a url or a local file path.
        :param referencing_schema_url: The url of the schema that is referencing the schema to download.
        """

        is_uri_remote = uri.startswith("http") or referencing_uri.startswith("http")

        # if the uri is local and the referencing uri is remote, then build the absolute uri from the two
        if referencing_uri.startswith("http") and not uri.startswith("http"):
            uri = urllib.parse.urljoin(referencing_uri, uri)

        # if the uri is not remote, then it is a local file path
        # make the file path absolute
        if not is_uri_remote:
            referencing_dir = os.path.dirname(referencing_uri)
            uri = os.path.abspath(os.path.join(referencing_dir, uri))

        file_name = self.uri_to_filename(uri)

        # check if the schema is already in the cache
        if file_name in self.__filenames:
            return

        is_cached = file_name in os.listdir(self.cache_location)

        if DEBUG:  # pragma: no cover
            print(
                f"[File Manager] uri: {uri}, file_name: {file_name}, is_cached: {is_cached}, is_uri_remote: {is_uri_remote}, referencing_uri: {referencing_uri}"
            )

        if is_cached:
            # load the schema from the cache
            with open(os.path.join(self.cache_location, file_name), "rb") as f:
                xsd_content: bytes = f.read()

        elif is_uri_remote:
            # if the file is online, load it from the url
            # if the uri is a local file path, but the referencing uri is online, then build the absolute uri from the two
            xsd_content = self.__download_and_store(uri, file_name)
        else:
            # otherwise the file is local and we can load it directly
            referencing_dir = os.path.dirname(referencing_uri)
            uri = os.path.join(referencing_dir, uri)

            if not os.path.isfile(uri):
                raise ValueError(
                    f"Could not find file {uri}, even though the XBRL report refers to it. The referencing file is {referencing_uri}"
                )

            with open(uri, "rb") as f:
                xsd_content = f.read()

        # parse the schema
        if DEBUG:  # pragma: no cover
            print(f"[File Manager] parsing {file_name}")

        try:
            xsd_tree = lxml.etree.parse(BytesIO(xsd_content), parser=self.__parser)
        except lxml.etree.XMLSyntaxError:
            raise ValueError(f"Failed to parse {uri} as an XML file. The file is not a valid XML file.")

        if not isinstance(xsd_tree, lxml.etree._ElementTree):
            raise ValueError(f"Failed to parse {uri} as an XML file. The file is not a valid XML file.")
        # load it into the cache
        self.__file_cache[file_name] = xsd_tree
        # add it to the list of filenames
        self.__filenames.append(file_name)
        # add it to the list of prefixes

        reference_uris: set[str] = set()
        # find all hrefs in the file
        # TODO: maybe make namespace non-hardcoded
        for href_elem in xsd_tree.findall(".//*[@xlink:href]", namespaces={"xlink": "http://www.w3.org/1999/xlink"}):
            # get the href attribute
            if not isinstance(href_elem, lxml.etree._Element):
                continue

            href = href_elem.get("{http://www.w3.org/1999/xlink}href", "")
            href = cast(str, href)

            # get the prefix under which the schema is loaded
            if "#" in href:
                href_uri, _ = href.split("#")
            else:
                href_uri = href

            if href_uri != "":
                reference_uris.add(href_uri)

        # find all schemaLocations in the file
        schemaLocation_elems = xsd_tree.xpath("//*[@schemaLocation]")
        if not isinstance(schemaLocation_elems, list):
            raise ValueError(
                f"schemaLocation_elems is not a list of lxml.etree._Element. It is a {type(schemaLocation_elems)}"
            )

        for schemaLocation_elem in schemaLocation_elems:
            if not isinstance(schemaLocation_elem, lxml.etree._Element):
                continue
            # get the schemaLocation attribute
            schemaLocation = schemaLocation_elem.get("schemaLocation", "")

            schemaLocation = cast(str, schemaLocation)
            # split the schemaLocation by whitespace

            if schemaLocation != "":
                reference_uris.add(schemaLocation)

        if DEBUG:  # pragma: no cover
            print(f"[File Manager] uri {uri} references {reference_uris}")

        for reference_uri in reference_uris:
            # load the schema
            self.__load_dts(reference_uri, referencing_uri=uri)
