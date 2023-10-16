import lxml
import lxml.etree
from pybr import QName

class PyBRConcept:
    """
    Class for representing an XBRL concept.
    A contains the following information:
    - id: str. The concept's id.
    - abstract: bool. Whether the concept is abstract or not.
    - name: str. The concept's name.
    - nillable: bool. Whether the concept is nillable or not.
    - substitution_group: str. The concept's substitution group.
    - type: str. The concept's type. Used for validation.
    - period_type: str. The concept's period type. Used for validation.
    TODO: create a class called PyBRReportElement. PyBRConcept should inherit from it.
    """

    __concept_cache: dict[QName, "PyBRConcept"] = {}

    def __init__(self, qname: QName, **kwargs) -> None:
        self.__qname : QName = qname

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.__concept_cache[qname] = self

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, concept_qname: QName) -> "PyBRConcept":
        """
        Create a PyBRConcept from an lxml.etree._Element.
        """
        # extract qname attributes from the xml element
        # concept_id = xml_element.attrib["id"]
        
        # create a QName object
        # concept_qname: QName concept_qname.copy()

        # extract the metadata attributes from the xml element
        other_attributes = {key: value for key, value in xml_element.attrib.items() if key not in ["id", "name"]}

        # instantiate the PyBRConcept object
        return cls(concept_qname, **other_attributes)

    def __str__(self) -> str:
        return self.__qname.get()
    
    def get_name(self) -> QName:
        return self.__qname
    