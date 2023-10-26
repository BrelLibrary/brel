import lxml
import lxml.etree
from pybr import PyBRAspect, QName
from pybr.characteristics import PyBRICharacteristic

class PyBREntityCharacteristic(PyBRICharacteristic):
    """
    Class for representing an XBRL entity.
    An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
    Additional information about the company can be found in the entity's segment.
    """
    __entity_cache = {}

    def __init__(self, qname: QName) -> None:
        self.__qname = qname

        self.__entity_cache[qname] = self
    
    def get_aspect(self) -> PyBRAspect:
        """
        returns the aspect of the entity characteristic, which is PyBRAspect.ENTITY
        @returns PyBRAspect: PyBRAspect.ENTITY
        """
        return PyBRAspect.ENTITY
    
    def get_value(self) -> QName:
        """
        returns the value of the entity characteristic, which is the entity's qname
        @info: the entity's qname consists of the entity's scheme and the entity's identifier
        @returns QName: the entity's qname
        """
        return self.__qname
    
    def get_schema(self) -> str:
        """
        returns the schema of the entity.
        The scheme is the url of the entity qname
        """
        return self.__qname.get_URL()

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBREntityCharacteristic":
        """
        Create a PyBREntity from an lxml.etree._Element.
        This is used for parsing characteristcs from an XBRL instance in XML format.
        @param xml_element: the lxml.etree._Element from which the PyBREntityCharacteristic is created
        @returns PyBREntityCharacteristic: the PyBREntityCharacteristic created from the lxml.etree._Element
        @raises ValueError: if the XML element is malformed
        """
        # first check if there is an identifier element
        identifier_element = xml_element.find("{*}identifier", namespaces=None)

        if identifier_element is None:
            raise ValueError("Could not find identifier element in entity characteristic")
        
        # then check if there is a scheme attribute
        if "scheme" not in identifier_element.attrib:
            raise ValueError("Could not find scheme attribute in identifier element")
        

        entity_id = xml_element.find("{*}identifier", namespaces=None).text

        # get the scheme of the entity. its an attribute of the xml element.
        entity_url = xml_element.find("{*}identifier", namespaces=None).get("scheme")
        
        entity_prefix = QName.try_get_prefix_from_url(entity_url)

        if entity_prefix is None:
            raise ValueError(f"Could not find prefix for entity URL: {entity_url}")
        
        entity_qname = QName(entity_url, entity_prefix, entity_id)

        if entity_id in cls.__entity_cache:
            return cls.__entity_cache[entity_id]

        return cls(entity_qname)
    
    def __str__(self) -> str:
        """
        Represents the entity characteristic as a string
        @returns str: the entity characteristic's qname as a string. It is the entity scheme and the entity identifier
        """
        return self.__qname.__str__()