import lxml
import lxml.etree
from enum import Enum
from pybr import QName

class PyBRLabelRole(Enum):
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
    def from_url(url: str) -> 'PyBRLabelRole':
        """
        Given an url to a label role, return the corresponding PyBRLabelRole.
        @param url: str containing the url to the label role
        @return: PyBRLabelRole corresponding to the url
        """
                # get the role
        role = None

        # strip everything before the last slash
        url = url.split("/")[-1]

        # iterate over enum and find the role
        for role_candidate in PyBRLabelRole:
            if role_candidate.value == url:
                role = role_candidate
                break
        
        # check if the role was found
        if role is None:
            raise ValueError(f"Could not find the role {url}")
        
        return role


class PyBRLabel():
    """ Represents a label in XBRL."""

    def __init__(self, text: str, language: str, role: PyBRLabelRole = PyBRLabelRole.STANDARD_LABEL) -> None:
        self.__text: str = text
        self.__language: str = language
        self.__role: PyBRLabelRole = role

    def __str__(self) -> str:
        return self.__text
    
    # first class citizens
    def get_language(self) -> str:
        return self.__language

    def get_role(self) -> PyBRLabelRole:
        return self.__role
    
    # internal methods
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element):
        """
        Create a PyBRLabel from an lxml.etree._Element.
        """
        nsmap = QName.get_nsmap()

        # get the text
        text = xml_element.text

        # get the language
        language = xml_element.attrib.get(f"{{{nsmap['xml']}}}lang")

        # get the role
        role = PyBRLabelRole.from_url(xml_element.attrib.get(f"{{{nsmap['xlink']}}}role"))

        return cls(text, language, role)
    

