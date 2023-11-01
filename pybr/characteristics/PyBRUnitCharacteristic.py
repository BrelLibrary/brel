import lxml
import lxml.etree
from pybr import PyBRAspect, QName
from pybr.characteristics import PyBRICharacteristic

class PyBRUnitCharacteristic(PyBRICharacteristic):
    """
    Class for representing an XBRL unit.
    It consists of and some stuff that I have not implemented yet
    """
    __unit_cache: dict[QName, 'PyBRUnitCharacteristic'] = {}

    def __init__(self, name: QName, numerators: list[QName], denominators: list[QName]) -> None:
        """
        Create a PyBRUnit.
        @param name: the name of the unit given as a QName
        @param numerators: the numerators of the unit given as a list of QNames
        @param denominators: the denominators of the unit given as a list of QNames
        """

        self.__name: QName = name
        self.__numerators = numerators
        self.__denominators = denominators

        self.__unit_cache[name] = self
    
    # first class citizens
    def get_aspect(self) -> PyBRAspect:
        """
        @returns PyBRAspect: returns PyBRAspect.UNIT
        """
        return PyBRAspect.UNIT
    
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
    
    def is_simple(self) -> bool:
        """
        A unit is simple if it has exactly one numerator and no denominators
        @return: True 'IFF' the unit is simple, False otherwise
        """
        return len(self.__numerators) == 1 and len(self.__denominators) == 0
        

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRUnitCharacteristic":
        """
        Create a PyBRUnit from an xml subtree.
        @param xml_element: the xml subtree from which the PyBRUnit is created
        @returns PyBRUnit: the PyBRUnit created from the xml subtree
        @raises ValueError: if the XML element is malformed
        """
        # Check if the xml element has an id attribute
        if "id" not in xml_element.attrib:
            raise ValueError("The xml element does not have an id attribute")

        # Turn the unit id into a QName
        unit_id_str = xml_element.attrib["id"]

        nsmap = QName.get_nsmap()

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
            unit_url = nsmap.get(None)
        
        # TODO: Implement parsing numerators and denominators
        numerators = []
        denominators = []
        
        unit_qname = QName(unit_url, unit_prefix, unit_id)

        if unit_qname in cls.__unit_cache:
            return cls.__unit_cache[unit_qname]

        return cls(unit_qname, numerators, denominators)
    
