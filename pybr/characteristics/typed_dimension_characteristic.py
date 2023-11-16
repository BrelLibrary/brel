import lxml
import lxml.etree
# from pybr import PyBRAspect, qname
# from pybr.characteristics import i_characteristic
# from pybr.reportelements import PyBRDimension, PyBRMember

# TODO: comes after report elements. so this can import report elements vanilla
from pybr import QName
from pybr.characteristics import PyBRAspect, PyBRICharacteristic
from pybr.reportelements import PyBRDimension, PyBRMember


class PyBRTypedDimensionCharacteristic(PyBRICharacteristic):
    """
    Class for representing an explicit dimension characteristic.
    An explicit dimension characteristic assigns a member-value to a dimension-aspect.
    """

    def __init__(self, dimension: PyBRDimension, value, aspect: PyBRAspect) -> None:
        self.__dimension: PyBRDimension = dimension
        self.__value = value
        self.__aspect: PyBRAspect = aspect
    
    # first class citizens
    def get_aspect(self) -> PyBRAspect:
        """
        returns the aspect of the explicit dimension characteristic.
        @info: Both typed and explicit dimension characteristics are not statically bound to an aspect.
        @returns PyBRAspect: the aspect of the explicit dimension characteristic.
        """
        return self.__aspect
    
    def get_value(self) -> PyBRMember:
        """
        returns the value of the explicit dimension characteristic.
        Values of explicit dimension characteristics are members.
        @returns PyBRMember: the member of the explicit dimension characteristic.
        """
        return self.__value
    
    def get_dimension(self) -> PyBRDimension:
        """
        returns the name/dimension/axis of the explicit dimension characteristic.
        Names of explicit dimension characteristics are dimensions.
        @returns PyBRDimension: the dimension of the explicit dimension characteristic.
        """
        return self.__dimension
    
    # second class citizens
    def __str__(self) -> str:
        """
        returns a string representation of the explicit dimension characteristic.
        This representation is the QName of the member.
        @returns str: member's QName
        """
        return self.__value.__str__()
    
    def __eq__(self, __value: object) -> bool:
        """
        returns whether the explicit dimension characteristics are equal.
        Explicit dimension characteristics are equal if their dimension, member and aspect are equal.
        @returns bool: whether the explicit dimension characteristics are equal.
        """
        if isinstance(__value, PyBRTypedDimensionCharacteristic):
            return self.__dimension == __value.__dimension and self.__aspect == __value.__aspect and self.__value == __value.__value
        else:
            return False
    
    # internal methods
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, dimension: PyBRDimension, value) -> "PyBRTypedDimensionCharacteristic":
        """
        Create a PyBRDimension from an lxml.etree._Element.
        @param xml_element: the xml subtree from which the PyBRDimension is created
        @param dimension: the dimension of the explicit dimension characteristic
        @param member: the member of the explicit dimension characteristic
        @returns PyBRExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
        @raises ValueError: if the XML element is malformed
        """
        # first check if there is a dimension attribute
        if "dimension" not in xml_element.attrib:
            raise ValueError("Could not find dimension attribute in explicit dimension characteristic")
        
        # then parse and create the dimension aspect
        dimension_axis = xml_element.attrib["dimension"]
        dimension_aspect = PyBRAspect.from_QName(QName.from_string(dimension_axis))

        return cls(dimension, value, dimension_aspect)