import lxml
import lxml.etree

from brel import QName, QNameNSMap
from brel.characteristics import BrelAspect, ICharacteristic

class UnitCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL unit.
    It consists of and some stuff that I have not implemented yet
    """
    __unit_cache: dict[QName, 'UnitCharacteristic'] = {}

    def __init__(self, name: QName, numerators: list[QName], denominators: list[QName]) -> None:
        """
        Create a Unit.
        @param name: the name of the unit given as a QName
        @param numerators: the numerators of the unit given as a list of QNames
        @param denominators: the denominators of the unit given as a list of QNames
        """

        self.__name: QName = name
        self.__numerators = numerators
        self.__denominators = denominators

        self.__unit_cache[name] = self
    
    # first class citizens
    def get_aspect(self) -> BrelAspect:
        """
        @returns Aspect: returns Aspect.UNIT
        """
        return BrelAspect.UNIT
    
    def get_numerators(self) -> list[QName]:
        """
        @returns list[QName]: the numerators of the unit
        """
        return self.__numerators
    
    def get_denominators(self) -> list[QName]:
        """
        @returns list[QName]: the denominators of the unit
        """
        return self.__denominators
    
    def get_value(self) -> QName:
        """
        @returns QName: the name of the unit
        @info: this is different from the numerators/denominators of the unit
        """
        return self.__name
    
    # second class citizens
    def __str__(self) -> str:
        """
        @returns str: the local name of the unit
        """
        # return self.__name.__str__()
        # it's probably better to just return the localname of the unit
        return self.__name.__str__()
    
    def __eq__(self, __value: object) -> bool:
        """
        @returns bool: True 'IFF' the unit is equal to the given value
        """
        if not isinstance(__value, UnitCharacteristic):
            return False
        
        return self.__name == __value.__name
    
    def is_simple(self) -> bool:
        """
        A unit is simple if it has exactly one numerator and no denominators
        @return: True 'IFF' the unit is simple, False otherwise
        """
        return len(self.__numerators) == 1 and len(self.__denominators) == 0
        

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap) -> "UnitCharacteristic":
        """
        Create a Unit from an xml subtree.
        @param xml_element: the xml subtree from which the Unit is created
        @returns Unit: the Unit created from the xml subtree
        @raises ValueError: if the XML element is malformed
        """
        # Check if the xml element has an id attribute
        if "id" not in xml_element.attrib:
            raise ValueError("The xml element does not have an id attribute")

        # Turn the unit id into a QName
        unit_id_str = xml_element.attrib["id"]

        nsmap = qname_nsmap.get_nsmap()

        # TODO: This feels a bit hacky. Improve this.
        if ":" in unit_id_str:
            unit_url = unit_id_str.split(":")[0]
            unit_id = unit_id_str.split(":")[1]

            unit_prefix = ""
            for prefix, url in nsmap.items():
                if url == unit_url:
                    unit_prefix = prefix
                    break
        else:
            unit_prefix = "xbrli"
            unit_id = unit_id_str
            unit_url = nsmap.get(unit_prefix)
        
        # TODO: Implement parsing numerators and denominators
        numerators = []
        denominators = []

        unit_qname = QName.from_string(f"{unit_prefix}:{unit_id}", qname_nsmap)

        if unit_qname in cls.__unit_cache:
            return cls.__unit_cache[unit_qname]

        return cls(unit_qname, numerators, denominators)
    
