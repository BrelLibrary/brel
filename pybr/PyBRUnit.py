import lxml
import lxml.etree
from pybr import PyBRAspect

class PyBRUnit(PyBRAspect):
    """
    Class for representing an XBRL unit.
    It consists of and some stuff that I have not implemented yet
    """
    # TODO: Units can be more complex than just a measure. Implement that.
    __unit_cache = {}

    def __init__(self, id) -> None:
        self.id = id

        self.__unit_cache[id] = self

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRUnit":
        """
        Create a PyBRUnit from an lxml.etree._Element.
        """
        unit_id = xml_element.attrib["id"]

        if unit_id in cls.__unit_cache:
            return cls.__unit_cache[unit_id]

        return cls(unit_id)

    def __str__(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.__str__()