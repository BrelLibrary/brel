import lxml
import lxml.etree
from brel import QName, QNameNSMap
from brel.resource import IResource


class BrelFootnote(IResource):
    """
    Represents a Reference in XBRL.
    References are used to link to external resources such as legal documents.
    """

    def __init__(self, label: str, role: str, content: str) -> None:
        self.__content: str = content
        self.__role: str = role
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

    # internal methods
    @classmethod
    def from_xml(
        cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap
    ) -> "BrelFootnote":
        """
        Create a BrelResource from an lxml.etree._Element.
        """
        nsmap = qname_nsmap.get_nsmap()

        # get the label
        label = xml_element.attrib.get(f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(
                f"Could not find the label of the resource {xml_element}"
            )
        if not isinstance(label, str):
            raise ValueError(
                f"The label of the resource {xml_element} is not a string"
            )

        # get the role
        role = xml_element.attrib.get(f"{{{nsmap['xlink']}}}role")
        if role is None:
            raise ValueError(
                f"Could not find the role of the resource {xml_element}"
            )
        if not isinstance(role, str):
            raise ValueError(
                f"The role of the resource {xml_element} is not a string"
            )

        # get the content. it might be a str or xhtml. If its xhtml, we need to convert it to str
        content = xml_element.text
        if content is None:
            raise ValueError(
                f"Could not find the content of the resource {xml_element}"
            )
        if not isinstance(content, str):
            raise ValueError(
                f"The content of the resource {xml_element} is not a string"
            )

        return cls(label, role, content)
