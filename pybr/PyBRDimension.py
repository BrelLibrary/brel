import lxml
import lxml.etree
from pybr import PyBRAspect, QName

class PyBRDimension(PyBRAspect):
    """
    Class for representing an XBRL dimension.
    A dimension is a concept that is used to add additional information to a fact.
    It contains the following information:
    - axis: the axis along which the dimension is defined
    - value: at what position along the axis the dimension is defined
    """

    def __init__(self, axis : QName, value) -> None:
        self.__axis : QName = axis
        self.__name = value
        self.__aspect = PyBRAspect(self.__axis.__str__(), [])
    
    def get_aspect(self) -> PyBRAspect:
        return self.__aspect
    
    def get_name(self):
        return self.__name
    
    def __str__(self) -> str:
        return self.__name
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRDimension":
        """
        Create a PyBRDimension from an lxml.etree._Element.
        """
        dimension_axis = xml_element.attrib["dimension"]
        dimension_value = xml_element.text

        return cls(dimension_axis, dimension_value)
    