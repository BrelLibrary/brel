import lxml
import lxml.etree
from pybr import PyBRAspect, QName
from pybr.characteristics import PyBRICharacteristic

class PyBRUnitCharacteristic(PyBRICharacteristic):
    """
    Class for representing an XBRL unit.
    It consists of and some stuff that I have not implemented yet
    """
    # TODO: Units can be more complex than just a measure. Implement that.
    __unit_cache = {}

    def __init__(self, name: QName, numerators: list[QName], denominators: list[QName]) -> None:
        self.__name: QName = name
        self.__numerators = numerators
        self.__denominators = denominators

        self.__unit_cache[name] = self
    
    # first class citizens
    def get_aspect(self) -> PyBRAspect:
        return PyBRAspect.UNIT
    
    def get_numerators(self) -> list[QName]:
        return self.__numerators
    
    def get_denominators(self) -> list[QName]:
        return self.__denominators
    
    def get_value(self) -> QName:
        return self.__name
    
    # second class citizens
    def __str__(self) -> str:
        # return self.__name.__str__()
        # it's probably better to just return the localname of the unit
        # TODO: think about this once more
        return self.__name.get_local_name()
    
    def is_simple(self) -> bool:
        """
        returns True 'IFF' the unit is simple, False otherwise
        A unit is simple if it has exactly one numerator and no denominators
        @ return: bool
        """
        return len(self.__numerators) == 1 and len(self.__denominators) == 0
        

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRUnitCharacteristic":
        """
        Create a PyBRUnit from an lxml.etree._Element.
        """
        # Turn the unit id into a QName
        unit_id_str = xml_element.attrib["id"]

        nsmap = QName.get_nsmap()

        # TODO: This is a bit hacky. Improve this.
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
        
        numerators = []
        denominators = []

        
        unit_qname = QName(unit_url, unit_prefix, unit_id)

        if unit_qname in cls.__unit_cache:
            return cls.__unit_cache[unit_id]

        return cls(unit_qname, numerators, denominators)
    
