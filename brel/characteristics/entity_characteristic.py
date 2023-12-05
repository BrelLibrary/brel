import lxml
import lxml.etree
# from pybr import Aspect, QName
# from pybr.characteristics import ICharacteristic
from ..qname import QName
from .pybr_aspect import BrelAspect
from .i_characteristic import ICharacteristic
from typing import cast

class EntityCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL entity.
    An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
    Additional information about the company can be found in the entity's segment.
    """
    __entity_cache: dict[QName, 'EntityCharacteristic'] = {}

    def __init__(self, qname: QName) -> None:
        self.__qname = qname

        self.__entity_cache[qname] = self

    # first class citizens    
    def get_aspect(self) -> BrelAspect:
        """
        returns the aspect of the entity characteristic, which is Aspect.ENTITY
        @returns Aspect: Aspect.ENTITY
        """
        return BrelAspect.ENTITY
    
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
    
    def __eq__(self, __value: object) -> bool:
        """
        compares the entity characteristic to another entity characteristic
        @param __value: the entity characteristic to compare to
        @returns bool: True if the entity characteristics are equal, False otherwise
        """
        if not isinstance(__value, EntityCharacteristic):
            return False
        else:
            return self.__qname == __value.__qname
    
    # internal methods
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "EntityCharacteristic":
        """
        Create a Entity from an lxml.etree._Element.
        This is used for parsing characteristcs from an XBRL instance in XML format.
        @param xml_element: the lxml.etree._Element from which the EntityCharacteristic is created
        @returns EntityCharacteristic: the EntityCharacteristic created from the lxml.etree._Element
        @raises ValueError: if the XML element is malformed
        """
        # first check if there is an identifier element
        identifier_element = xml_element.find("{*}identifier", namespaces=None)

        if identifier_element is None:
            raise ValueError("Could not find identifier element in entity characteristic")
        
        # then check if there is a scheme attribute
        if "scheme" not in identifier_element.attrib:
            raise ValueError("Could not find scheme attribute in identifier element")
        

        entity_id_elem = xml_element.find("{*}identifier", namespaces=None)
        # The identifier element is guaranteed according to the XBRL 2.1 specification to have a text element
        entity_id_elem = cast(lxml.etree._Element, entity_id_elem)
        entity_id = entity_id_elem.text
        # The text is guaranteed to have at least length 1 according to the XBRL 2.1 spec
        entity_id = cast(str, entity_id)

        entity_url = entity_id_elem.get("scheme")
        # The scheme is required by the XBRL 2.1 spec
        entity_url = cast(str, entity_url) 
        
        entity_prefix = QName.get_prefix_from_url(entity_url)

        if entity_prefix is None:
            raise ValueError(f"Could not find prefix for entity URL: {entity_url}")
        
        QName.add_to_nsmap(entity_url, entity_prefix)
        
        entity_qname = QName.from_string(f"{entity_prefix}:{entity_id}")

        if entity_id in cls.__entity_cache:
            return cls.__entity_cache[entity_qname]

        return cls(entity_qname)
    
    def __str__(self) -> str:
        """
        Represents the entity characteristic as a string
        @returns str: the entity characteristic's qname as a string. It is the entity scheme and the entity identifier
        """
        return self.__qname.__str__()