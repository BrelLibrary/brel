"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from typing import Mapping, cast
from brel.qnames.qname import QName
import lxml.etree
from lxml.etree import _Element, _ElementTree  # type: ignore

from brel.qnames.qname_utils import (
    is_namespace_localname_notation,
    qname_from_str,
)


def has_str_attribute(element: _Element, attribute: str | QName) -> bool:
    """
    Helper function for checking if an element has a string attribute.
    :param element: lxml.etree.Element to check
    :param attribute: str containing the name of the attribute
    :returns: bool indicating if the attribute is present
    """
    if isinstance(attribute, QName):
        attribute = attribute.clark_notation()
    elif is_namespace_localname_notation(attribute):
        attribute = qname_from_str(attribute, element).clark_notation()

    return attribute in element.attrib


def get_str_attribute(
    element: _Element, attribute: str | QName, default: str | None = None
) -> str:
    """
    Helper function for getting a string attribute from an element. Always returns a string.
    :param element: lxml.etree.Element to get the attribute from
    :param attribute: str containing the name of the attribute
    :param default: str containing the default value to return if the attribute is not found
    :return: str containing the value of the attribute
    :raises: if the attribute is not found and no default value is provided
    :raises: if the attribute is not a string
    """
    if isinstance(attribute, QName):
        attribute = attribute.clark_notation()
    elif is_namespace_localname_notation(attribute):
        attribute = qname_from_str(attribute, element).clark_notation()

    value = element.attrib.get(attribute)
    if value is None:
        if default is not None:
            return default

        raise ValueError(f"{attribute} attribute not found on element {element}")
    return value


def get_str_attribute_optional(element: _Element, attribute: str | QName) -> str | None:
    """
    Helper function for getting a string attribute from an element. Returns None if the attribute is not found.
    :param element: lxml.etree.Element to get the attribute from
    :param attribute: str containing the name of the attribute
    :return: str containing the value of the attribute
    :raises: if the attribute is not a string
    """
    if isinstance(attribute, QName):
        attribute = attribute.clark_notation()
    elif is_namespace_localname_notation(attribute):
        attribute = qname_from_str(attribute, element).clark_notation()

    return element.attrib.get(attribute)


def get_str_tag(element: _Element) -> str:  # type: ignore
    """
    Helper function for getting the tag of an element as a string.
    :param element: lxml.etree.Element to get the tag from
    :returns: str containing the tag of the element
    """
    return element.tag


def find_elements(
    element: _ElementTree | _Element,  # type: ignore
    xpath_query: str | QName,
) -> list[_Element]:
    if isinstance(xpath_query, QName):
        xpath_query = xpath_query.prefix_local_name_notation()

    if isinstance(element, _ElementTree):
        element = element.getroot()

    nsmap: Mapping[str, str] = {k: v for k, v in element.nsmap.items() if k is not None}
    try:
        # return element.findall(xpath_query, namespaces=nsmap)
        result = element.xpath(
            xpath_query,
            namespaces=nsmap,
        )
        if not isinstance(result, list):
            raise TypeError("XPath query did not return a list")
        if not all(isinstance(e, _Element) for e in result):
            raise TypeError("XPath query returned a non-element")
        return result  # type: ignore
    except lxml.etree.XPathEvalError:
        return []


def find_element(
    element: _ElementTree | _Element,  # type: ignore
    xpath_query: str | QName,
) -> _Element | None:
    if isinstance(xpath_query, QName):
        xpath_query = xpath_query.prefix_local_name_notation()

    if isinstance(element, _ElementTree):
        element = element.getroot()

    nsmap: Mapping[str, str] = {k: v for k, v in element.nsmap.items() if k is not None}
    return element.find(xpath_query, namespaces=nsmap)


def get_element(
    element: _ElementTree | _Element,  # type: ignore
    xpath_query: str | QName,
) -> _Element:
    found_element = find_element(element, xpath_query)
    if found_element is None:
        raise ValueError(f"Element not found for xpath {xpath_query}")
    return found_element


def get_all_nsmaps(
    lxml_etrees: list[lxml.etree._ElementTree],  # type: ignore
) -> list[dict[str, str]]:
    """
    Given a list of lxml etree objects, get all the namespace mappings.
    :param lxml_etrees: A list of lxml etree objects.
    :returns: A list of namespace mappings.
    """
    nsmaps: list[dict[str, str]] = []
    for lxml_etree in lxml_etrees:
        for xmlElement in lxml_etree.iter():
            nsmap: dict[str | None, str] = xmlElement.nsmap
            nsmap.update(
                {
                    str(key.replace("xmlns:", "")): str(value)  # type: ignore
                    for key, value in xmlElement.attrib.items()
                    if key.startswith("xmlns:")  # type: ignore
                }
            )

            nsmap.pop(None, None)

            nsmap_typecasted = cast(dict[str, str], nsmap)
            nsmaps.append(nsmap_typecasted)

    return nsmaps
