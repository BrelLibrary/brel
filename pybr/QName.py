class QName:
    __namespace_url_map : dict[str, str] = {}
    __url_namespace_map : dict[str, str] = {}

    def __init__(self, uri : str, prefix : str, local_name : str):
        self.__uri : str = uri
        self.__prefix : str = prefix
        self.__local_name : str = local_name

        if uri not in QName.__namespace_url_map and prefix not in QName.__url_namespace_map:
            QName.__namespace_url_map[uri] = prefix
            QName.__url_namespace_map[prefix] = uri
    
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
            return self.__uri == __value.get_URL() and self.__local_name == __value.get_local_name()
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
        # check if the string contains an URL or a prefix
        if "{" in qname_string:
            # the string contains an URL
            # extract the URL and the local name
            url, local_name = qname_string[1:].split("}")
            # get the prefix from the namespace map
            prefix = cls.__namespace_url_map[url]
        else:
            # the string contains a prefix
            # extract the prefix and the local name
            prefix, local_name = qname_string.split(":")
            # get the URL from the prefix map
            url = cls.__url_namespace_map[prefix]
        
        # create the QName object
        return cls(url, prefix, local_name)