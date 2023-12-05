import validators
import re

class QName:
    __url_to_prefix : dict[str, str] = {}
    __prefix_to_url : dict[str, str] = {}
    __prefix_redirects : dict[str, str] = {}

    def __init__(self, uri : str, prefix : str, local_name : str):
        if prefix in QName.__prefix_redirects:
            print("WARNING: The prefix", prefix, "is a prefix redirect. It will be redirected to", QName.__prefix_redirects[prefix])
            prefix = QName.__prefix_redirects[prefix]
        
        self.__uri : str = uri
        self.__prefix : str = prefix
        self.__local_name : str = local_name

        self.add_to_nsmap(uri, prefix)


        self.__uri : str = uri
        self.__prefix : str = prefix
        self.__local_name : str = local_name
    
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
    def from_string(cls, qname_string : str) -> "QName":
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

            if not validators.url(url):
                raise ValueError(f"Invalid QName string: {qname_string}. URL is not valid")
            # get the prefix from the namespace map
            if url not in cls.__url_to_prefix:
                raise ValueError(f"Invalid QName string: {qname_string}. URL not found in namespace map")
            prefix = cls.__url_to_prefix[url]
        elif ":" in qname_string:
            # the string contains a prefix
            # extract the prefix and the local name
            prefix, local_name = qname_string.split(":", 1)
            # get the URL from the prefix map
            if prefix not in cls.__prefix_to_url and prefix not in cls.__prefix_redirects:
                raise ValueError(f"Invalid QName string: {qname_string}. Prefix not found in namespace map")
            elif prefix in cls.__prefix_to_url:
                url = cls.__prefix_to_url[prefix]
            else:
                url = cls.__prefix_to_url[cls.__prefix_redirects[prefix]]
        else:
            raise ValueError(f"Invalid QName string: {qname_string}")
        
        if ":" in local_name:
            raise ValueError(f"Invalid QName string: {qname_string}. Local name contains a ':'")
        
        # create the QName object
        return cls(url, prefix, local_name)
    
    @classmethod
    def is_str_qname(cls, qname_string : str) -> bool:
        """
        Checks if a string is a valid QName
        """
        if isinstance(qname_string, QName):
            return True
        if not isinstance(qname_string, str):
            return False
        try:
            cls.from_string(qname_string)
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

            if len(section) > 0 and "www" not in section:
                prefix = section
                
        return prefix
    
    @classmethod
    def get_nsmap(cls) -> dict[str, str]:
        """
        Returns the namespace map
        """
        return cls.__prefix_to_url
    
    @classmethod
    def add_to_nsmap(cls, url : str, prefix : str):
        """
        Adds a prefix to the namespace map
        @param url: str containing the URL
        @param prefix: str containing the prefix
        @raises ValueError: if the URL or the prefix is already in the namespace map, but mapped to a different prefix or URL
        """
        if not validators.url(url):
            raise ValueError(f"Invalid URL: {url}. Maybe you switched the URL and the namespace?")
        
        if prefix is None:
            raise ValueError("The namespace cannot be None")
        
        # Ask Ghislain about this
        if url in cls.__url_to_prefix or prefix in cls.__prefix_to_url:
            if prefix in cls.__prefix_to_url and cls.__prefix_to_url[prefix] != url:
                # the prefix is already in the namespace map, but it is mapped to a different URL
                raise ValueError(f"The prefix {prefix} is already in the namespace map, but it is mapped to a different URL")
            elif url in cls.__url_to_prefix and cls.__url_to_prefix[url] != prefix:
                # the URL is already in the namespace map, but it is mapped to a different prefix
                raise ValueError(f"The URL {url} is already in the namespace map, but it is mapped to a different namespace.\nOld namespace: {cls.__url_to_prefix[url]}\nNew namespace: {prefix}")
            else:
                # there is no conflict, but the prefix or the URL is already in the namespace map
                # so just return
                return

        cls.__url_to_prefix[url] = prefix
        cls.__prefix_to_url[prefix] = url
    
    @classmethod
    def set_redirect(cls, redirect_from: str, redirect_to: str):
        """
        Sets the prefix redirects. This means that if a QName is created with the prefix redirect as prefix, the prefix will be replaced with the redirect destination.
        @param redirect_from: str containing the prefix that should be redirected
        @param redirect_to: str containing the prefix that should be redirected to
        @raises ValueError: if the redirect destination does not exist in the namespace map or if the redirect source already exists in the namespace map
        """
        if redirect_to not in cls.__prefix_to_url:
            raise ValueError(f"Invalid prefix redirect: {redirect_to}. The redirect destination does not exist in the namespace map")
        if redirect_from in cls.__prefix_to_url:
            raise ValueError(f"Invalid prefix redirect: {redirect_from}. The redirect source already exists in the namespace map")
