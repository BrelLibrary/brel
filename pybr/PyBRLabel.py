import lxml
import lxml.etree
from enum import Enum
from pybr import QName

class PyBRLabelRole(Enum):
    STANDARD_LABEL = 1

    DOCUMENTATION = 101
    TERSE = 102
    VERBOSE = 103
    DEFINITION_GUIDANCE = 104
    DISCLOSURE_GUIDANCE = 105
    PRESENTATION_GUIDANCE = 106
    MEASUREMENT_GUIDANCE = 107
    COMMENTARY_GUIDANCE = 108
    EXAMPLE_GUIDANCE = 109

    PERIOD_START_LABEL = 201
    PERIOD_END_LABEL = 202
    TOTAL_LABEL = 203
    NET_LABEL = 204
    NEGATED_LABEL = 205

    POSITIVE_LABEL = 301
    NEGATIVE_LABEL = 302
    ZERO_LABEL = 303

    DEPRECATED_LABEL = 401
    DEPRECATED_DATE_LABEL = 402
    RESTATED_LABEL = 403


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
        # TODO: default language?
        language = xml_element.attrib.get(f"{{{nsmap['xml']}}}lang")

        # get the role
        # TODO: implement this properly
        role = PyBRLabelRole.STANDARD_LABEL

        return cls(text, language, role)

