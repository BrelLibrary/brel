"""
This module contains the BrelLabel class, which represents a label in XBRL.

=================

- author: Robin Schmidiger
- version: 0.4
- date: 21 January 2024

=================
"""

from enum import Enum
from typing import cast

import lxml
import lxml.etree

from brel import QName, QNameNSMap
from brel.resource import IResource


class BrelLabel(IResource):
    """Represents a label in XBRL."""

    STANDARD_LABEL_ROLE = "http://www.xbrl.org/2003/role/label"

    def __init__(
        self,
        text: str,
        label: str,
        language: str,
        label_role: str = STANDARD_LABEL_ROLE,
    ) -> None:
        self.__text: str = text
        self.__language: str = language
        self.__label_role: str = label_role
        # Note: the Brellabel's label is not the same as the Brellabel's text.
        # BrelLabels with different roles can have different texts, but the same label.
        self.__label: str = label

    def __str__(self) -> str:
        return self.__text

    # first class citizens
    def get_language(self) -> str:
        return self.__language

    def get_label_role(self) -> str:
        return self.__label_role

    def get_label(self) -> str:
        return self.__label

    def get_role(self) -> str:
        return self.__label_role

    def get_title(self) -> str | None:
        return None

    def get_content(self) -> dict:
        return {None: self.__text}

    # internal methods
    @classmethod
    def from_xml(
        cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap
    ) -> "BrelLabel":
        """
        Create a BrelLabel from an lxml.etree._Element.
        :param xml_element: lxml.etree._Element containing the xml element
        :qname_nsmap: QNameNSMap containing the namespace map
        :returns BrelLabel: created from the xml element
        :raises ValueError: if the language of the label could not be found.
        """
        nsmap = qname_nsmap.get_nsmap()

        # get the text. The text of the label is optional.
        text = xml_element.text
        if text is None:
            text = ""

        # In xml, the language of an element is inherited from its parent if it is not specified.
        lang_element: lxml.etree._Element | None = xml_element
        language: str | bytes | None = None
        # Step up the tree until the language is found or the root is reached.
        while language is None and lang_element is not None:
            language = lang_element.attrib.get(f"{{{nsmap['xml']}}}lang")
            lang_element = lang_element.getparent()

        # Language is required. If it is not found, raise an error.
        if language is None:
            raise ValueError(f"Could not find the language for the label {text}")
        language = cast(str, language)

        # get the role. If the role is not specified, it is assumed to be a standard label.
        role_str = xml_element.attrib.get(f"{{{nsmap['xlink']}}}role")
        if role_str is None:
            role = BrelLabel.STANDARD_LABEL_ROLE
        else:
            role_str = cast(str, role_str)
            role = role_str

        # get the label. This attribute is required.
        label = xml_element.attrib.get(f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(f"label attribute not found on element {xml_element}")
        label = cast(str, label)

        return cls(text, label, language, role)
