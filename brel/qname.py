"""
This module contains the QName class and the QNameNSMap class.
The QName class represents a qualified name.
The QNameNSMap class represents a namespace map.

@author: Robin Schmidiger
@version: 0.5
@date: 18 December 2023
"""

import re
from editdistance import eval as editdistance
from collections import defaultdict

class QNameNSMap:
    def __init__(self) -> None:
        self.__url_to_prefix : dict[str, str] = {}
        self.__prefix_to_url : dict[str, str] = {}
        self.__prefix_redirects : dict[str, str] = {}
        self.__prefix_renames : dict[str, list[str]] = defaultdict(list)
    
    def add_to_nsmap(self, url : str, prefix : str):
        """
        Adds a prefix to the namespace map
        @param url: str containing the URL
        @param prefix: str containing the prefix
        @raises ValueError: if the URL or the prefix is already in the namespace map, but mapped to a different prefix or URL
        """
        # if not validators.url(url):
        #     print (f"WARNING: Invalid URL: {url}. Maybe you switched the URL and the namespace?")
        if "http" not in url:
            print(f"WARNING: Invalid URL: {url}. Maybe you switched the URL and the namespace?")

        if prefix is None:
            raise ValueError("The namespace cannot be None")
        
        # Ask Ghislain about this
        if url in self.__url_to_prefix or prefix in self.__prefix_to_url:
            if prefix in self.__prefix_to_url and self.__prefix_to_url[prefix] != url:
                # the prefix is already in the namespace map, but it is mapped to a different URL
                print(f"original url: {self.__prefix_to_url[prefix]}")
                print(f"new url: {url}")
                # raise ValueError(f"The prefix {prefix} is already in the namespace map, but it is mapped to a different URL")
            elif url in self.__url_to_prefix and self.__url_to_prefix[url] != prefix:
                # the URL is already in the namespace map, but it is mapped to a different prefix
                # raise ValueError(f"The URL {url} is already in the namespace map, but it is mapped to a different namespace.\nOld namespace: {self.__url_to_prefix[url]}\nNew namespace: {prefix}")
                pass
            else:
                # there is no conflict, but the prefix or the URL is already in the namespace map
                # so just return
                return

        self.__url_to_prefix[url] = prefix
        self.__prefix_to_url[prefix] = url

    def add_redirect(self, redirect_from: str, redirect_to: str):
        """
        Sets the prefix redirects. This means that if a QName is created with the prefix redirect as prefix, the prefix will be replaced with the redirect destination.
        @param redirect_from: str containing the prefix that should be redirected
        @param redirect_to: str containing the prefix that should be redirected to
        @raises ValueError: if the redirect destination does not exist in the namespace map or if the redirect source already exists in the namespace map
        """
        if redirect_to not in self.__prefix_to_url:
            raise ValueError(f"Invalid prefix redirect: {redirect_to}. The redirect destination does not exist in the namespace map")
        if redirect_from in self.__prefix_to_url:
            raise ValueError(f"Invalid prefix redirect: {redirect_from}. The redirect source already exists in the namespace map")
        self.__prefix_redirects[redirect_from] = redirect_to
    
    def get_redirect(self, redirect_from: str) -> str | None:
        """
        Gets the redirect destination for a prefix redirect
        @param redirect_from: str containing the prefix that should be redirected
        @return: str containing the prefix that should be redirected to
        """
        if redirect_from in self.__prefix_redirects:
            return self.__prefix_redirects[redirect_from]
        else:
            return None
    
    def add_rename(self, rename_from: str, rename_to: str):
        """
        Sets the prefix renames. This means that if a QName is created with the prefix rename_from, the prefix will be replaced with the rename_to.
        @param rename_from: str containing the prefix that should be renamed
        @param rename_to: str containing the prefix that should be renamed to
        @raises ValueError: if the rename destination does not exist in the namespace map or if the rename source already exists in the namespace map
        """
        if rename_to not in self.__prefix_to_url:
            raise ValueError(f"Invalid prefix rename: {rename_to}. The rename destination does not exist in the namespace map")
        if rename_from not in self.__prefix_to_url:
            raise ValueError(f"Invalid prefix rename: {rename_from}. The rename source does not exist in the namespace map")
        self.__prefix_renames[rename_from].append(rename_to)
    
    def get_renames(self, rename_from: str) -> list[str]:
        """
        Gets the rename destinations for a prefix rename
        @param rename_from: str containing the prefix that should be renamed
        @return: list[str] containing the prefixes that should be renamed to
        """
        if rename_from in self.__prefix_renames:
            return self.__prefix_renames[rename_from]
        else:
            return []
    
    def get_prefix(self, url: str) -> str | None:
        """
        Gets the prefix for a URL
        @param url: str containing the URL
        @return: str containing the prefix
        """
        if url in self.__url_to_prefix:
            return self.__url_to_prefix[url]
        else:
            return None
        
    def get_url(self, prefix: str) -> str | None:
        """
        Gets the URL for a prefix
        @param prefix: str containing the prefix
        @return: str containing the URL
        """
        if prefix in self.__prefix_to_url:
            return self.__prefix_to_url[prefix]
        else:
            return None

    def get_nsmap(self) -> dict[str, str]:
        """
        Returns the namespace map
        """
        return self.__prefix_to_url

class QName:

    def __init__(self, uri : str, prefix : str, local_name : str, nsmap : QNameNSMap):
        self.__nsmap = nsmap
        redirect = nsmap.get_redirect(prefix)
        if redirect is not None:
            print("WARNING: The prefix", prefix, "is a prefix redirect. It will be redirected to", redirect)
            prefix = redirect
        
        
        self.__uri : str = uri
        self.__prefix : str = prefix
        self.__local_name : str = local_name

        self.__nsmap.add_to_nsmap(uri, prefix)
    
    def get_URL(self):
        return self.__uri
    
    def get_prefix(self):
        return self.__prefix
    
    def get_local_name(self):
        return self.__local_name
    
    def get(self) -> str:
        """
        returns a string representation of the qualified name
        it does not substitute the prefix with the URI
        example: us-gaap:Assets
        """
        return f"{self.__prefix}:{self.__local_name}"
    
    def __str__(self):
        return self.get()
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, QName):
            result = self.__uri == __value.get_URL() and self.__local_name == __value.get_local_name()
            # if not result and self.__prefix == __value.get_prefix() and self.__local_name == __value.get_local_name():
            #     print(f"WARNING: The two QNames {self} and {__value} are not equal, but they have the same prefix and local name")
            #     print(f"The first QName has the URL {self.__uri} and the second QName has the URL {__value.get_URL()}")
            return result 

        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self.__uri) + hash(self.__local_name)
    
    def resolve(self):
        """
        returns a string representation of the qualified name
        it substitutes the prefix with the URI
        example: {http://www.xbrl.org/2003/instance}Assets
        """
        return f"{{{self.__uri}}}{self.__local_name}"
    
    @classmethod
    def from_string(cls, qname_string : str, nsmap: QNameNSMap) -> "QName":
        """
        Creates a QName from a string representation of a QName
        The string representation must be in one of the following formats:
        - {URL}local_name
        - prefix:local_name
        Furthermore, The prefix and the URL must be known. So there must be an entry in the namespace map for the prefix and the URL.
        @param qname_string: str containing the string representation of the QName
        @returns QName: the QName created from the string representation
        @raises ValueError: if the string representation is not valid or if the prefix or the URL is not known
        """
        # check if the string contains an URL or a prefix
        if "}" in qname_string and "{" not in qname_string:
            raise ValueError(f"Invalid QName string: {qname_string}." + "The string contains a '}' but no '{'")
        elif "}" not in qname_string and "{" in qname_string:
            raise ValueError(f"Invalid QName string: {qname_string}." + "The string contains a '{' but no '}'")
        elif "{" in qname_string and "}" in qname_string and qname_string.index("{") == 0 and qname_string.index("}") > 0:
            # the string contains an URL
            # extract the URL and the local name
            url, local_name = qname_string[1:].split("}")

            # Note: according to the SEC, the URL must not necessarily be a valid URL
            # if not validators.url(url):
            #     raise ValueError(f"Invalid QName string: {qname_string}. URL is not valid")
            # get the prefix from the namespace map
            prefix = nsmap.get_prefix(url)
            if prefix is None:
                raise ValueError(f"Invalid QName string: {qname_string}. URL not found in namespace map")

        elif ":" in qname_string:
            # raise DeprecationWarning("QName string contains a ':' but no '{' or '}'. This is deprecated. Use the format {URL}local_name instead")
            # the string contains a prefix
            # extract the prefix and the local name
            prefix, local_name = qname_string.split(":", 1)
            # get the URL from the prefix map
            nsmap_redirect = nsmap.get_redirect(prefix)
            if nsmap_redirect is not None:
                prefix = nsmap_redirect

            nsmap_url = nsmap.get_url(prefix)
            if nsmap_url is None:
                raise ValueError(f"Invalid QName string: {qname_string}. Prefix not found in namespace map")
            else:
                url = nsmap_url
            
        else:
            raise ValueError(f"Invalid QName string: {qname_string}")
        
        if ":" in local_name:
            raise ValueError(f"Invalid QName string: {qname_string}. Local name contains a ':'")
        
        # create the QName object
        return cls(url, prefix, local_name, nsmap)
    
    @classmethod
    def is_str_qname(cls, qname_string : str, nsmap: QNameNSMap) -> bool:
        """
        Checks if a string is a valid QName
        """
        if isinstance(qname_string, QName):
            return True
        if not isinstance(qname_string, str):
            return False
        try:
            cls.from_string(qname_string, nsmap)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_version_from_url(url: str) -> str | None:

        version = ""
        sections = url.split("/")
        for section in sections:
            section = re.sub(r'[^0-9]', '', section)
            if section.isnumeric():
                version = section
        
        return version
    
    @staticmethod
    def get_prefix_from_url(url: str):
        prefix = ""
        sections = url.split("/")
        for section in sections:
            section = re.sub(r'[^a-zA-Z]', '', section)
            section = section.replace("xsd", "")
            section = section.replace("xml", "")           

            if len(section) > 0 and "www" not in section:
                prefix = section
                
        return prefix
    
    def get_nsmap(self) -> QNameNSMap:
        """
        Returns the namespace map
        """
        return self.__nsmap
    
    @classmethod
    def from_xpointer(cls, xpointer: str, nsmap: QNameNSMap) -> 'QName':
        """
        Creates a QName from an xpointer string. It must be given in xpointer shorthand notation.
        @param xpointer: str containing the xpointer
        @return: QName created from the xpointer
        """

        if "#" not in xpointer:
            raise ValueError(f"Invalid xpointer: {xpointer}. The xpointer does not contain a '#'")
        
        if "_" not in xpointer:
            raise ValueError(f"Invalid xpointer: {xpointer}. The xpointer does not contain a '_'")

        qname_uri = None

        uri, fragment_identifier = xpointer.split("#", 1)
        prefix, local_name = fragment_identifier.split("_", 1)

        if uri.startswith("http://") or uri.startswith("https://"):
            suggested_uri = uri.rsplit("/", 1)[0]
            potential_uris = nsmap.get_nsmap().values()
            qname_uri = min(potential_uris, key=lambda potential_uri: editdistance(potential_uri, suggested_uri))
        else:
            # This should not happen except if whoever made the filing is an absolute idiot
            # it means that in the QName namespace map, there is a prefix that maps to the local file system.
            # The local file system is then associated with a prefix

            possible_prefixes = [prefix] + nsmap.get_renames(prefix)

            for possible_prefix in possible_prefixes:
                if not possible_prefix.startswith("http://") and not possible_prefix.startswith("https://"):
                    qname_uri = nsmap.get_url(possible_prefix)
                    break

        if qname_uri is None:
            raise ValueError(f"Invalid xpointer: {xpointer}. The xpointer does not contain a valid URL")
        
        return QName.from_string(f"{{{qname_uri}}}{local_name}", nsmap)