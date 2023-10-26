import lxml
import lxml.etree
from pybr import PyBRAspect, QName
from pybr.characteristics import PyBRICharacteristic
from pybr.reportelements import PyBRDimension, PyBRMember

class PyBRExplicitDimensionCharacteristic(PyBRICharacteristic):
    """
    Class for representing an XBRL dimension.
    A dimension is a concept that is used to add additional information to a fact.
    It contains the following information:
    - axis: the axis along which the dimension is defined
    - value: at what position along the axis the dimension is defined
    """
    # TODO: write and update docstrings

    def __init__(self, dimension: PyBRDimension, member : PyBRMember, aspect: PyBRAspect) -> None:
        self.__dimension = dimension
        self.__member = member
        self.__aspect = aspect
    
    def get_aspect(self) -> PyBRAspect:
        return self.__aspect
    
    def get_value(self) -> PyBRMember:
        return self.__member
    
    def get_name(self) -> PyBRDimension:
        return self.__dimension
    
    def __str__(self) -> str:
        return self.__member.__str__()
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, dimension: PyBRDimension, member: PyBRMember) -> "PyBRExplicitDimensionCharacteristic":
        """
        Create a PyBRDimension from an lxml.etree._Element.
        """
        dimension_axis = xml_element.attrib["dimension"]
        # TODO: maybe instantiate the pybrmember in here instead of taking it as a "from_xml" argument
        dimension_value = xml_element.text

        dimension_aspect = PyBRAspect.from_QName(QName.from_string(dimension_axis))

        return cls(dimension, member, dimension_aspect)   