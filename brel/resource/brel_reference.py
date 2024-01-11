import lxml
import lxml.etree
from brel import QName, QNameNSMap
from brel.resource import IResource


class BrelReference(IResource):
    """
    Represents a Reference in XBRL.
    References are used to link to external resources such as legal documents.
    """

    def __init__(self, label: str, role: str, content: dict) -> None:
        self.__content: dict = content
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

    def get_content(self) -> dict:
        return self.__content

    # internal methods
    @classmethod
    def from_xml(
        cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap
    ) -> "BrelReference":
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

        # get the content. Parse it as a dict
        content = {}
        for child in xml_element:
            tag = child.tag

            # This part removes the url from the tag
            # this is theoretically safe since
            # - lxml translates all qname prefixes to their full url. In clark notation, that's {url}local_name
            # - valid urls cannot contain the character "}". So by finding the first "}" we can find the beginning of the local name
            if "}" in tag:
                tag = tag[tag.find("}") + 1 :]
            content[tag] = child.text

        return cls(label, role, content)
