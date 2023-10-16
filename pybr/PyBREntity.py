import lxml
from pybr import PyBRAspect

class PyBREntity(PyBRAspect):
    """
    Class for representing an XBRL entity.
    An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
    Additional information about the company can be found in the entity's segment.
    """
    # TODO: Improve this code. It doesn't work for all cases.

    __entity_cache = {}

    def __init__(self, identifier: str) -> None:
        self.__id = identifier

        self.__entity_cache[identifier] = self

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBREntity":
        """
        Create a PyBREntity from an lxml.etree._Element.
        """
        entity_id = xml_element.find("{*}identifier").text

        if entity_id in cls.__entity_cache:
            return cls.__entity_cache[entity_id]

        return cls(entity_id)
    
    def __str__(self) -> str:
        # TODO: Improve the __str__ method.
        # return self.identifier
        return f"Entity: {self.__id}"
    
    def get_name(self) -> str:
        return self.__id