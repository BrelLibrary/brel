import lxml
import lxml.etree
from enum import Enum
from brel import QName, QNameNSMap
from brel.resource import IResource
from typing import cast


class BrelLabelRole(Enum):
    STANDARD_LABEL = "label"

    DOCUMENTATION = "documentation"
    TERSE = "terseLabel"
    VERBOSE = "verboseLabel"
    DEFINITION_GUIDANCE = "definitionGuidance"
    DISCLOSURE_GUIDANCE = "disclosureGuidance"
    PRESENTATION_GUIDANCE = "presentationGuidance"
    MEASUREMENT_GUIDANCE = "measurementGuidance"
    COMMENTARY_GUIDANCE = "commentaryGuidance"
    EXAMPLE_GUIDANCE = "exampleGuidance"

    PERIOD_START_LABEL = "periodStartLabel"
    PERIOD_END_LABEL = "periodEndLabel"
    TOTAL_LABEL = "totalLabel"
    NET_LABEL = "netLabel"
    NEGATED_LABEL = "negatedLabel"

    POSITIVE_LABEL = "positiveLabel"
    NEGATIVE_LABEL = "negativeLabel"
    ZERO_LABEL = "zeroLabel"

    DEPRECATED_LABEL = "deprecatedLabel"
    DEPRECATED_DATE_LABEL = "deprecatedDateLabel"
    RESTATED_LABEL = "restatedLabel"
    ######################################

    COMMON_PRACTICE_LABEL = "commonPracticeLabel"
    NEGATED = "negated"
    NEGATED_TOTAL = "negatedTotal"
    NEGATED_NET_TOTAL = "negatedNetTotal"
    NEGATED_PERIOD_START = "negatedPeriodStart"
    NEGATED_PERIOD_END = "negatedPeriodEnd"
    NEGATED_PERIOD_START_LABEL = "negatedPeriodStartLabel"
    NEGATED_PERIOD_END_LABEL = "negatedPeriodEndLabel"
    NEGATED_TERSE_LABEL = "negatedTerseLabel"
    NEGATED_TOTAL_LABEL = "negatedTotalLabel"

    @staticmethod
    def from_url(url: str) -> "BrelLabelRole":
        """
        Given an url to a label role, return the corresponding BrelLabelRole.
        @param url: str containing the url to the label role
        @return: BrelLabelRole corresponding to the url
        """
        # get the role
        role = None

        # strip everything before the last slash
        url = url.split("/")[-1]

        # iterate over enum and find the role
        for role_candidate in BrelLabelRole:
            if role_candidate.value == url:
                role = role_candidate
                break

        # check if the role was found
        if role is None:
            raise ValueError(f"Could not find the role {url}")

        return role


class BrelLabel(IResource):
    """Represents a label in XBRL."""

    def __init__(
        self,
        text: str,
        label: str,
        language: str,
        label_role: BrelLabelRole = BrelLabelRole.STANDARD_LABEL,
    ) -> None:
        self.__text: str = text
        self.__language: str = language
        self.__label_role: BrelLabelRole = label_role
        # Note: the Brellabel's label is not the same as the Brellabel's text.
        # BrelLabels with different roles can have different texts, but the same label.
        self.__label: str = label

    def __str__(self) -> str:
        return self.__text

    # first class citizens
    def get_language(self) -> str:
        return self.__language

    def get_label_role(self) -> BrelLabelRole:
        return self.__label_role

    def get_label(self) -> str:
        return self.__label

    def get_role(self) -> str:
        return self.__label_role.value

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
        @param xml_element: lxml.etree._Element containing the xml element
        @qname_nsmap: QNameNSMap containing the namespace map
        @return: BrelLabel created from the xml element
        @raise ValueError: if the language of the label could not be found.
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
            raise ValueError(
                f"Could not find the language for the label {text}"
            )
        language = cast(str, language)

        # get the role. If the role is not specified, it is assumed to be a standard label.
        role_str = xml_element.attrib.get(f"{{{nsmap['xlink']}}}role")
        if role_str is None:
            role = BrelLabelRole.STANDARD_LABEL
        else:
            role_str = cast(str, role_str)
            role = BrelLabelRole.from_url(role_str)

        # get the label. This attribute is required.
        label = xml_element.attrib.get(f"{{{nsmap['xlink']}}}label")
        if label is None:
            raise ValueError(
                f"label attribute not found on element {xml_element}"
            )
        label = cast(str, label)

        return cls(text, label, language, role)
