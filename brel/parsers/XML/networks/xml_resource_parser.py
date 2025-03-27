"""
This module is responsible for parsing an XML element into an appropriate Brel resource.
Currently, the module can parse BrelLabel, BrelFootnote and BrelReference resources.

=================

- author: Robin Schmidiger
- version: 0.1
- date: 19 February 2024

=================
"""

import lxml
import lxml.etree

from brel import QNameNSMap, QName
from brel.resource import IResource, BrelFootnote, BrelLabel, BrelReference
from typing import cast, Mapping
from brel.parsers.utils.lxml_utils import get_str


def parse_xml_resource(xml_element: lxml.etree._Element, prefix_to_uri: Mapping[str, str]) -> IResource:
    """
    Create a BrelResource from an lxml.etree._Element.
    :param xml_element: the lxml.etree._Element from which the BrelResource is created
    :param prefix_to_uri: the mapping from prefix to uri
    :returns: the BrelResource created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """

    def clark(prefix: str, local_name: str) -> str:
        """
        Create a clark notation from a prefix and a local name.
        lxml uses clark notation to represent qnames.
        """
        return f"{{{prefix_to_uri[prefix]}}}{local_name}"

    def get_lang_recursive(xml_element: lxml.etree._Element) -> str:
        """
        Get the language of an xml element.
        If the language is not found, check the parent.
        """
        lang = xml_element.attrib.get(clark("xml", "lang"))
        if lang is not None:
            return lang

        parent = xml_element.getparent()
        if parent is not None:
            return get_lang_recursive(parent)
        raise ValueError(f"Could not find the language for the label {xml_element}")

    # first check if xlink:type == "resource"
    if xml_element.attrib.get(clark("xlink", "type")) != "resource":
        raise ValueError("The xlink:type is not resource")

    # get the label, role and tag
    label = get_str(xml_element, clark("xlink", "label"))
    role = get_str(xml_element, clark("xlink", "role"))
    tag = xml_element.tag

    # create the resource
    if "label" in tag:
        lang = get_lang_recursive(xml_element)
        text = xml_element.text
        if text is None:
            text = ""
        return BrelLabel(text, label, lang, role)
    elif "footnote" in tag:
        lang = get_lang_recursive(xml_element)
        text = xml_element.text
        if text is None:
            text = ""
            for child in xml_element:
                text += lxml.etree.tostring(child, encoding="unicode")
        return BrelFootnote(text, label, lang, role)
    elif "reference" in tag:
        # the children of a resource form a dict
        # turn the xml children into a dict. strip the namespace from the tag
        content: dict = {}
        for child in xml_element:
            child_tag = str(child.tag)
            if "}" in child_tag:
                child_tag = child_tag.split("}", 1)[1]
            content[child_tag] = child.text

        return BrelReference(content, label, role)
    else:
        raise ValueError(f"Unknown tag {tag}")
