"""
This module contains the QName class and the QNameNSMap class.
The QName class represents a qualified name.
The QNameNSMap class represents a namespace map.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 06 January 2024

====================
"""

import re
from collections import defaultdict


class QName:
    """
    This class represents a qualified name. Qualified names are used in XML and XBRL to identify elements.
    Brel re-uses qualified names to identify report elements, types, etc. in the report.
    A qualified name consists of a URI, a prefix and a local name.

    - The URI identifies the namespace of the element.
    - The prefix is a short string that is used to identify the namespace.
    - The local name is the name of the element within the namespace.

    An example of a qualified name is us-gaap:Assets.

    - The URI is http://fasb.org/us-gaap/2019-01-31
    - The prefix is us-gaap and acts as an abbreviation for the URI
    - The local name is Assets

    The #QName class is closely related to the #QNameNSMap class. The QNameNSMap class is used to map prefixes to URIs and vice versa.
    When creating a QName, sometimes either the prefix or the URI is unknown. In this case, the QNameNSMap class is used to find the missing information.
    There is usually only one QNameNSMap object per report. It is created when the report is created and then passed to the QName constructor.
    """

    def __init__(
        self, uri: str, prefix: str, local_name: str, nsmap: "QNameNSMap"
    ):
        """
        Creates a QName object.
        Note that this constructor changes the prefix if there is a prefix redirect in the #QNameNSMap.
        :param uri: str containing the URI. Must be a valid URL
        :param prefix: str containing the prefix
        :param local_name: str containing the local name
        :param nsmap: QNameNSMap containing the namespace map
        :raises ValueError: if there is a conflict with the namespace map
        """
        self.__nsmap = nsmap
        redirect = nsmap.get_redirect(prefix)
        if redirect is not None:
            print(
                "WARNING: The prefix",
                prefix,
                "is a prefix redirect. It will be redirected to",
                redirect,
            )
            prefix = redirect

        self.__uri: str = uri
        self.__prefix: str = prefix
        self.__local_name: str = local_name

        self.__nsmap.add_to_nsmap(uri, prefix)

    def get_URL(self) -> str:
        """
        :returns str: containing the URI
        """
        return self.__uri

    def get_prefix(self) -> str:
        """
        :returns str: containing the prefix
        """
        return self.__prefix

    def get_local_name(self) -> str:
        """
        :returns str: containing the local name
        """
        return self.__local_name

    def get_nsmap(self) -> "QNameNSMap":
        """
        :returns QNameNSMap: containing the namespace map.
        """
        return self.__nsmap

    def get(self) -> str:
        """
        :returns str: representation of the qualified name.
        it does not substitute the prefix with the URI.

        example: us-gaap:Assets
        """
        return f"{self.__prefix}:{self.__local_name}"

    def __str__(self) -> str:
        """
        :returns str: representation of the qualified name.
        Functionally equivalent to QName.get()
        """
        return self.get()

    def __eq__(self, __value: object) -> bool:
        """
        Checks if the QName self is equal to the QName __value.
        Two QNames are equal if
        - the local name is equal
        - the prefix is equal

        Note that the URI is not considered when checking for equality.
        This is because Brel does not allow two completely different URIs to map to the same prefix.
        Two URIs are completely different if they are not versions of the same URI.
        Example:
        - http://www.xbrl.org/2003/instance and http://www.xbrl.org/2020/instance are versions of the same URI.
        - http://www.xbrl.org/2003/instance and http://www.xbrl.org/2003/taxonomy are not versions of the same URI.

        :param __value: object containing the QName to compare with.
        :returns bool: True if __value is a QName and it is equal to self, False otherwise.
        """

        if isinstance(__value, QName):
            result = (
                self.__uri == __value.get_URL()
                and self.__local_name == __value.get_local_name()
            )
            # if not result and self.__prefix == __value.get_prefix() and self.__local_name == __value.get_local_name():
            #     print(f"WARNING: The two QNames {self} and {__value} are not equal, but they have the same prefix and local name")
            #     print(f"The first QName has the URL {self.__uri} and the second QName has the URL {__value.get_URL()}")
            return result

        else:
            return False

    def __hash__(self) -> int:
        """
        :returns int: containing the hash of the QName
        """
        return hash(self.__uri) + hash(self.__local_name)

    def resolve(self) -> str:
        """
        produces the clark notation of the qualified name
        it substitutes the prefix with the URI

        example: {http://www.xbrl.org/2003/instance}Assets

        :returns str: containing the clark notation of the qualified name
        """
        return f"{{{self.__uri}}}{self.__local_name}"

    @classmethod
    def from_string(cls, qname_string: str, nsmap: "QNameNSMap") -> "QName":
        """
        Creates a QName from a string representation of a QName
        The string representation must be in one of the following formats:
        - {URL}local_name
        - prefix:local_name
        Furthermore, The prefix and the URL must be known. So there must be an entry in the namespace map for the prefix and the URL.
        :param qname_string: str containing the string representation of the QName
        :param nsmap: QNameNSMap containing the namespace map
        :returns QName: the QName created from the string representation
        :raises ValueError: if the string representation is not valid or if the prefix or the URL is not known
        """
        # check if the string contains an URL or a prefix
        if "}" in qname_string and "{" not in qname_string:
            raise ValueError(
                f"Invalid QName string: {qname_string}."
                + "The string contains a '}' but no '{'"
            )
        elif "}" not in qname_string and "{" in qname_string:
            raise ValueError(
                f"Invalid QName string: {qname_string}."
                + "The string contains a '{' but no '}'"
            )
        elif (
            "{" in qname_string
            and "}" in qname_string
            and qname_string.index("{") == 0
            and qname_string.index("}") > 0
        ):
            # the string contains an URL
            # extract the URL and the local name
            url, local_name = qname_string[1:].split("}")

            # Note: according to the SEC, the URL must not necessarily be a valid URL
            # if not validators.url(url):
            #     raise ValueError(f"Invalid QName string: {qname_string}. URL is not valid")
            # get the prefix from the namespace map
            prefix = nsmap.get_prefix(url)
            if prefix is None:
                raise ValueError(
                    f"Invalid QName string: {qname_string}. URL not found in namespace map"
                )

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
                raise ValueError(
                    f"Invalid QName string: {qname_string}. Prefix not found in namespace map"
                )
            else:
                url = nsmap_url

        else:
            raise ValueError(f"Invalid QName string: {qname_string}")

        if ":" in local_name:
            raise ValueError(
                f"Invalid QName string: {qname_string}. Local name contains a ':'"
            )

        # create the QName object
        return cls(url, prefix, local_name, nsmap)

    @classmethod
    def is_str_qname(cls, qname_string: str, nsmap: "QNameNSMap") -> bool:
        """
        Checks if a string represents a QName and could be parsed by QName.from_string()
        :param qname_string: str containing the string representation of the QName
        :param nsmap: QNameNSMap containing the namespace map
        :returns bool: True if the string represents a QName, False otherwise
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


class QNameNSMap:
    """
    This class represents a namespace map used to map prefixes to URIs and vice versa.
    It is used by the #QName class to create QNames from strings.
    It requires a 1:1 mapping between prefixes and URIs.

    A QNameNSMap introduces two concepts to achieve this: prefix redirects and prefix renames.

    **Prefix redirects**

    For many reports, it is possible that the same namespace is used with different prefixes.
    For example, the namespace http://fasb.org/us-gaap/2020 is used with the prefixes us-gaap and us-gaap-ci.
    This is not allowed in Brel. So one of the prefixes must be redirected to the other.
    In case of the example above, the prefix us-gaap-ci must be redirected to us-gaap.
    This can be done as follows:
    ```
    nsmap.add_redirect("us-gaap-ci", "us-gaap")
    ```

    **Prefix renames**

    Sometimes, the same prefix is used for different namespaces.
    For example, the prefix 'types' is used for the namespaces http://fasb.org/us-types/2020 and http://fasb.org/uk-types/2020.
    This is not allowed in Brel. So one of the prefixes must be renamed.
    In case of the example above, the prefix 'types' could be renamed to 'us-types' or 'uk-types'.
    This can be done as follows:
    ```
    nsmap.rename("http://fasb.org/us-types/2020", "us-types")
    ```

    Now whenever a QName is created with the prefix 'namespaces', the prefix will be replaced with 'us-types'.
    """

    def __init__(self) -> None:
        """
        Creates a QNameNSMap object
        """
        self.__url_to_prefix: dict[str, str] = {}
        self.__prefix_to_url: dict[str, str] = {}
        self.__prefix_redirects: dict[str, str] = {}

    def add_to_nsmap(self, url: str, prefix: str) -> None:
        """
        Adds a prefix to the namespace map
        :param url: str containing the URL
        :param prefix: str containing the prefix
        :raises ValueError: if the URL/prefix is already in the namespace map, but mapped to a different prefix/URL than the one provided
        """
        if prefix is None:
            raise ValueError("The namespace cannot be None")

        if not isinstance(prefix, str):
            raise ValueError("The namespace must be a string")

        # check if the prefix is already in the namespace map
        if url in self.__url_to_prefix or prefix in self.__prefix_to_url:
            if (
                prefix in self.__prefix_to_url
                and self.__prefix_to_url[prefix] != url
            ):
                # the prefix is already in the namespace map, but it is mapped to a different URL
                raise ValueError(
                    f"The prefix {prefix} is already mapped to {self.__prefix_to_url[prefix]}, but you are trying to map it to {url}"
                )
            elif (
                url in self.__url_to_prefix
                and self.__url_to_prefix[url] != prefix
            ):
                # the URL is already in the namespace map, but it is mapped to a different prefix
                raise ValueError(
                    f"The URL {url} is already in the namespace map, but it is mapped to a different namespace.\nOld namespace: {self.__url_to_prefix[url]}\nNew namespace: {prefix}"
                )
            else:
                # there is no conflict, but the prefix or the URL is already in the namespace map
                # so just return
                return

        self.__url_to_prefix[url] = prefix
        self.__prefix_to_url[prefix] = url

    def add_redirect(self, redirect_from: str, redirect_to: str) -> None:
        """
        Adds a prefix redirect to the namespace map.
        When creating a new QName, the redirect_from prefix will be replaced with the redirect_to prefix.

        :param redirect_from: str containing the prefix that should be redirected
        :param redirect_to: str containing the prefix that should be redirected to
        :raises ValueError: if the redirect destination does not exist in the namespace map or if the redirect source already exists in the namespace map
        """
        if redirect_to not in self.__prefix_to_url:
            raise ValueError(
                f"Invalid prefix redirect: {redirect_to}. The redirect destination does not exist in the namespace map"
            )
        if redirect_from in self.__prefix_to_url:
            raise ValueError(
                f"Invalid prefix redirect: {redirect_from}. The redirect source already exists in the namespace map"
            )
        self.__prefix_redirects[redirect_from] = redirect_to

    def get_redirect(self, redirect_from: str) -> str | None:
        """
        Gets the redirect destination for a prefix redirect
        :param redirect_from: str containing the prefix that should be redirected
        :return str: containing the prefix that should be redirected to
        """
        if redirect_from in self.__prefix_redirects:
            return self.__prefix_redirects[redirect_from]
        else:
            return None

    def rename(self, rename_uri: str, rename_prefix: str) -> None:
        """
        Given a URI and a prefix, changes the mapping of the URI to the prefix.
        When creating a new QName and only the URI is known, the prefix will be replaced with the rename_prefix.
        :param rename_uri: str containing the URI
        :param rename_prefix: str containing the prefix
        :raises ValueError: if the URI does not exist in the namespace map
        """
        if rename_uri not in self.__url_to_prefix:
            raise ValueError(
                f"Invalid prefix rename: {rename_uri}. The URI does not exist in the namespace map"
            )
        self.__url_to_prefix[rename_uri] = rename_prefix
        self.__prefix_to_url[rename_prefix] = rename_uri

    def get_prefix(self, url: str) -> str | None:
        """
        Gets the prefix for a URL
        :param url: str containing the URL.
        :return str | None: The prefix for the URL. None if the URL is not in the namespace map
        """
        if url in self.__url_to_prefix:
            return self.__url_to_prefix[url]
        else:
            return None

    def get_url(self, prefix: str) -> str | None:
        """
        Gets the URL for a prefix
        :param prefix: str containing the prefix
        :return str | None: The URL for the prefix. None if the prefix is not in the namespace map
        """
        if prefix in self.__prefix_to_url:
            return self.__prefix_to_url[prefix]
        else:
            return None

    def get_nsmap(self) -> dict[str, str]:
        """
        Returns the namespace map as a dict.
        This is deprecated. Use QNameNSMap.get_prefix()
        :return dict[str, str]: containing the namespace map
        """
        return self.__prefix_to_url
