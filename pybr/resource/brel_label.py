import lxml
import lxml.etree
from enum import Enum
from pybr import QName
from pybr.resource import IResource

class BrelLabelRole(Enum):
    # TODO: test if the labels beside the standard label and terse label actually work
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
    def from_url(url: str) -> 'BrelLabelRole':
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
    """ Represents a label in XBRL."""

    def __init__(self, text: str, label: str, language: str, label_role: BrelLabelRole = BrelLabelRole.STANDARD_LABEL) -> None:
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
    
    def get_role(self) -> str | None:
        return self.__label_role.value
    
    def get_title(self) -> str | None:
        return None
    
    def get_content(self) -> dict:
        return {None: self.__text}
    
    # internal methods
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element):
        """
        Create a BrelLabel from an lxml.etree._Element.
        """
        nsmap = QName.get_nsmap()

        # get the text
        text = xml_element.text

        # get the binding to the xml schema instance namespace
        # there is a xmlns:xml attribute that binds the 'xml' prefix to the xml schema instance namespace
        # so get the namespaces that are bound to the 'xml' prefix in the children of the current element

        # get the language
        # language = xml_element.attrib.get(f"{{{nsmap['xml']}}}lang")
        # filter through all attributes and get the one ending with 'lang'
        # language = None
        # for attribute in xml_element.attrib:
        #     if attribute.endswith("lang"):
        #         language = xml_element.attrib[attribute]
        #         break
        
        # language = next(filter(lambda attribute: attribute.endswith("lang"), xml_element.attrib), None)
        language = xml_element.attrib.get(f"{{{nsmap['xml']}}}lang")
        
        if language is None:
            raise ValueError(f"Could not find the language for the label {text}")

        # get the role
        role = BrelLabelRole.from_url(xml_element.attrib.get(f"{{{nsmap['xlink']}}}role"))

        # get the label
        label = xml_element.attrib.get(f"{{{nsmap['xlink']}}}label")

        return cls(text, label, language, role)
    

