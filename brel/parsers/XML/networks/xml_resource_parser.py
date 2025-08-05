"""
=================

- author: Robin Schmidiger
- version: 0.3
- date: 9 May 2025

=================
"""

import re
from lxml.etree import _Element  # type: ignore

from brel.resource import IResource, BrelFootnote, BrelLabel, BrelReference
from brel.parsers.utils.lxml_utils import (
    get_elem_lang_recursive,
    get_str_attribute,
    get_clark_notation_tag,
)

def parse_xml_resource(xml_element: _Element) -> IResource:
    if get_str_attribute(xml_element, "xlink:type") != "resource":
        raise ValueError("The xlink:type is not resource")

    label = get_str_attribute(xml_element, "xlink:label")
    role = get_str_attribute(xml_element, "xlink:role")
    tag = get_clark_notation_tag(xml_element)

    if "label" in tag:
        lang = get_elem_lang_recursive(xml_element)
        text = xml_element.text if xml_element.text else ""
        return BrelLabel(text, label, lang, role)
    elif "footnote" in tag:
        lang = get_elem_lang_recursive(xml_element)
        text = xml_element.text or "".join(child.__str__() for child in xml_element)
        return BrelFootnote(text, label, lang, role)
    elif "reference" in tag:
        content = {
            re.sub(r"^\{.*\}", "", child.tag): child.text for child in xml_element
        }
        return BrelReference(content, label, role)
    else:
        raise ValueError(f"Unknown tag {tag}")
