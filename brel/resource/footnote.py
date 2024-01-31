import lxml
import lxml.etree

from brel import QName, QNameNSMap
from brel.resource import IResource
from typing import cast


class BrelFootnote(IResource):
    """
    Represents a Reference in XBRL.
    References are used to link to external resources such as legal documents.
    """

    def __init__(self, label: str, language: str, role: str, content: str) -> None:
        self.__content: str = content
        self.__role: str = role
        self.__language: str = language
        self.__label: str = label

    def __str__(self) -> str:
        return str(self.__content)

    # first class citizens
    def get_role(self) -> str | None:
        return self.__role

    def get_label(self) -> str:
        return self.__label

    def get_title(self) -> str | None:
        return None

    def get_content(self) -> str:
        return self.__content

    def get_language(self) -> str:
        return self.__language

    # internal methods
    @classmethod
    def from_xml(
        cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap
    ) -> "BrelFootnote":
        """
        Create a BrelResource from an lxml.etree._Element.
        """
        nsmap = qname_nsmap.get_nsmap()

        # In xml, the language of an element is inherited from its parent if it is not specified.
        lang_element: lxml.etree._Element | None = xml_element
        language: str | bytes | None = None
        # Step up the tree until the language is found or the root is reached.
        while language is None and lang_element is not None:
            language = lang_element.attrib.get(f"{{{nsmap['xml']}}}lang")
            lang_element = lang_element.getparent()

        # Language is required. If it is not found, raise an error.
        if language is None:
            raise ValueError(f"Could not find the language for the label {xml_element}")
        language = cast(str, language)

        # get the label
        label = xml_element.attrib.get(f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(f"Could not find the label of the resource {xml_element}")
        if not isinstance(label, str):
            raise ValueError(f"The label of the resource {xml_element} is not a string")

        # get the role
        role = xml_element.attrib.get(f"{{{nsmap['xlink']}}}role")
        if role is None:
            raise ValueError(f"Could not find the role of the resource {xml_element}")
        if not isinstance(role, str):
            raise ValueError(f"The role of the resource {xml_element} is not a string")

        # get the content.
        content = xml_element.text
        # if the content is None, try getting the embedded content
        if content is None:
            # parse the children as xhtml
            content = ""
            for child in xml_element:
                content += lxml.etree.tostring(child, encoding="unicode")

        if content is None:
            raise ValueError(
                f"Could not find the content of the resource {xml_element}"
            )
        if not isinstance(content, str):
            raise ValueError(
                f"The content of the resource {xml_element} is not a string"
            )

        return cls(label, language, role, content)
