import validators

class QName:
    __url_to_namespace : dict[str, str] = {}
    __namespace_to_url : dict[str, str] = {}

    def __init__(self, uri : str, prefix : str, local_name : str):
        self.__uri : str = uri
        self.__prefix : str = prefix
        self.__local_name : str = local_name

        if uri not in QName.__url_to_namespace and prefix not in QName.__namespace_to_url:
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
        if self.__prefix:
            return f"{self.__prefix}:{self.__local_name}"
        else:
            return self.__local_name
    
    def __str__(self):
        return self.get()
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, QName):
            result = self.__uri == __value.get_URL() and self.__local_name == __value.get_local_name()
            if not result and self.__prefix == __value.get_prefix() and self.__local_name == __value.get_local_name():
                print(f"WARNING: The two QNames {self} and {__value} are not equal, but they have the same prefix and local name")
                print(f"The first QName has the URL {self.__uri} and the second QName has the URL {__value.get_URL()}")
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
        """
        # TODO: This constructor is UNSAFE. There might be a case where the namespace map is not complete. So QName.__url_namespace_map[prefix] and QName.__namespace_url_map[uri] might raise KeyErrors    
        # check if the string contains an URL or a prefix
        if "{" in qname_string and "}" in qname_string and qname_string.index("{") == 0 and qname_string.index("}") > 0:
            # the string contains an URL
            # extract the URL and the local name
            url, local_name = qname_string[1:].split("}")
            # get the prefix from the namespace map
            if url not in cls.__url_to_namespace:
                raise ValueError(f"Invalid QName string: {qname_string}. URL not found in namespace map")
            prefix = cls.__url_to_namespace[url]
        elif ":" in qname_string:
            # the string contains a prefix
            # extract the prefix and the local name
            prefix, local_name = qname_string.split(":")
            # get the URL from the prefix map
            if prefix not in cls.__namespace_to_url:
                raise ValueError(f"Invalid QName string: {qname_string}. Prefix not found in namespace map")
            url = cls.__namespace_to_url[prefix]
        else:
            raise ValueError(f"Invalid QName string: {qname_string}")
        
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
    def try_get_prefix_from_url(url : str) -> str | None:
        """
        Tries to generate a prefix from an URL
        @param url: The URL
        @return: A string representing the prefix or None if no prefix could be generated
        """

        # check if the URL is valid
        if not validators.url(url):
            print(f"[QName.try_get_prefix_from_url()] Invalid URL: {url}")
            return None
        
        # see if the URL is already in the namespace map
        if url in QName.__url_to_namespace:
            return QName.__url_to_namespace[url]
        
        # split the URL into parts using "/" as the separator
        url_parts = url.split("/")
        # the last part of the url that is not a number is the prefix
        prefix = None
        for part in url_parts[::-1]:
            if not part.isnumeric():
                prefix = part
                break
        
        # if the prefix is an URL, then it is not a valid prefix
        if validators.url(prefix):
            return None
        
        # if the prefix is an empty string, then it is not a valid prefix
        if prefix == "":
            return None
        
        return prefix
    
    @classmethod
    def get_nsmap(cls) -> dict[str, str]:
        """
        Returns the namespace map
        """
        return cls.__namespace_to_url
    
    @classmethod
    def add_to_nsmap(cls, url : str, namespace : str):
        """
        Adds a prefix to the namespace map
        """
        if not validators.url(url):
            raise ValueError(f"Invalid URL: {url}. Maybe you switched the URL and the namespace?")
        
        if namespace is None:
            return
        
        # TODO: This method is UNSAFE. There might be a case where the namespace map is not complete. So QName.__url_namespace_map[prefix] and QName.__namespace_url_map[uri] might raise KeyErrors
        # Ask Ghislain about this
        if url in cls.__url_to_namespace or namespace in cls.__namespace_to_url:
            if namespace in cls.__namespace_to_url and cls.__namespace_to_url[namespace] != url:
                print(f"WARNING: The namespace {namespace} is already in the namespace map, but it is mapped to a different URL")
                print(f"Old URL: {cls.__namespace_to_url[namespace]}")
                print(f"New URL: {url}")
                print(f"The namespace {namespace} will be mapped to the old URL")
            return

        cls.__url_to_namespace[url] = namespace
        cls.__namespace_to_url[namespace] = url
