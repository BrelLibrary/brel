"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

import lxml.etree
import re

from brel.parsers.utils.optional_utils import get_or_raise
from brel.qnames.qname import QName


def qname_from_str(
    qname_str: str,
    referencing_element: lxml.etree._Element,  # type: ignore
) -> QName:
    """
    Converts a string to a QName object.
    :param qname_str: The string to convert. It can be in the format "{namespace}local_name" or "namespace:local_name".
    :param referencing_element: The lxml.etree._Element to use as the base for the QName.
    :returns: The QName object.
    :raises ValueError: If the string is not in the correct format or if the namespace URI is not found.
    """
    if is_clark_notation(qname_str):
        return qname_from_clark_notation(qname_str, referencing_element)
    elif is_namespace_localname_notation(qname_str):
        return qname_from_namespace_localname_notation(qname_str, referencing_element)
    else:
        return qname_from_local_name_only(qname_str, referencing_element)


def is_clark_notation(clark_str: str) -> bool:
    """
    Check if a string is in the clark notation format.
    :param clark_str: The string to check.
    :returns: True if the string is in clark notation, False otherwise.
    """
    expression = r"^\{([^\}]+)\}([^\{]+)$"
    match = re.match(expression, clark_str)
    return match is not None


def qname_from_clark_notation(clark_str: str, referencing_element: lxml.etree._Element) -> QName:  # type: ignore
    """
    Converts a string to a QName object.
    :param clark_str: The string to convert. It should be in the format "{namespace}local_name" aka. the clark notation.
    :param referencing_element: The lxml.etree._Element to use as the base for the QName.
    :returns: The QName object.
    :raises ValueError: If the string is not in the correct format or if the namespace URI is not found.
    """
    expression = r"^\{([^\}]+)\}([^\{]+)$"
    match = re.match(expression, clark_str)

    if match:
        uri = match.group(1)
        local_name = match.group(2)
        inverted_nsmap = {v: k for k, v in referencing_element.nsmap.items()}
        inverted_nsmap["http://www.w3.org/XML/1998/namespace"] = "xml"
        prefix = inverted_nsmap.get(uri, None)

        if prefix is None:
            raise ValueError(
                f"Namespace URI {uri} not found in the element's namespace map."
            )

        return QName(uri, prefix, local_name)
    else:
        raise ValueError(f"String '{clark_str}' is not in the correct QName format.")


def to_clark_notation(url: str, local_name: str) -> str:
    """
    Given a prefix, a local name and a prefix to URL mapping, return the clark notation.
    :param prefix: The prefix.
    :param local_name: The local name.
    :returns: The clark notation.
    """
    return f"{{{url}}}{local_name}"


def is_namespace_localname_notation(namespace_localname_str: str) -> bool:
    """
    Check if a string is in the namespace:local_name format.
    :param namespace_localname_str: The string to check.
    :returns: True if the string is in namespace:local_name format, False otherwise.
    """
    expression = r"^([^\:]+)\:([^\:]+)$"
    match = re.match(expression, namespace_localname_str)
    return match is not None


def qname_from_namespace_localname_notation(
    namespace_localname_notation: str,
    referencing_element: lxml.etree._Element,  # type: ignore
) -> QName:
    """
    Converts a string in the format "namespace:local_name" to a QName object.
    :param namespace_localname_notation: The string to convert. It should be in the format "namespace:local_name".
    :param referencing_element: The lxml.etree._Element to use as the base for the QName.
    :returns: The QName object.
    :raises ValueError: If the string is not in the correct format or if the namespace URI is not found.
    """
    expression = r"^([^\:]+)\:([^\:]+)$"
    match = re.match(expression, namespace_localname_notation)

    if match:
        prefix = match.group(1)
        local_name = match.group(2)
        nsmap = referencing_element.nsmap
        nsmap["xml"] = "http://www.w3.org/XML/1998/namespace"
        uri = nsmap.get(prefix, None)

        if uri is None:
            raise ValueError(
                f"Namespace prefix '{prefix}' not found in the element's namespace map."
            )

        return QName(uri, prefix, local_name)
    else:
        raise ValueError(
            f"String '{namespace_localname_notation}' is not in the correct namespace:local_name format."
        )


def to_namespace_localname_notation(namespace: str, local_name: str) -> str:
    """
    Given a namespace and a local name, return the namespace:local_name format.
    :param namespace: The namespace.
    :param local_name: The local name.
    :returns: The namespace:local_name format.
    """
    return f"{namespace}:{local_name}"


def qname_from_local_name_only(
    local_name: str,
    referencing_element: lxml.etree._Element,  # type: ignore
) -> QName:
    """
    Converts a string in the format "local_name" to a QName object.
    :param local_name: The string to convert. It should be in the format "local_name".
    :param referencing_element: The lxml.etree._Element to use as the base for the QName.
    :returns: The QName object.
    """
    uri = get_or_raise(
        referencing_element.nsmap.get(None),
        ValueError(
            f"{local_name} is not a valid QName since has neither prefix nor a default namespace"
        ),
    )
    return QName(uri, "", local_name)
