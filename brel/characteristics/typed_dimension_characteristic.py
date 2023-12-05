import lxml
import lxml.etree

from brel import QName
from brel.characteristics import BrelAspect, ICharacteristic
from brel.reportelements import Dimension, Member


class TypedDimensionCharacteristic(ICharacteristic):
    """
    Class for representing an explicit dimension characteristic.
    An explicit dimension characteristic assigns a member-value to a dimension-aspect.
    """

    def __init__(self, dimension: Dimension, value, aspect: BrelAspect) -> None:
        self.__dimension: Dimension = dimension
        self.__value = value
        self.__aspect: BrelAspect = aspect
    
    # first class citizens
    def get_aspect(self) -> BrelAspect:
        """
        returns the aspect of the explicit dimension characteristic.
        @info: Both typed and explicit dimension characteristics are not statically bound to an aspect.
        @returns Aspect: the aspect of the explicit dimension characteristic.
        """
        return self.__aspect
    
    def get_value(self) -> Member:
        """
        returns the value of the explicit dimension characteristic.
        Values of explicit dimension characteristics are members.
        @returns Member: the member of the explicit dimension characteristic.
        """
        return self.__value
    
    def get_dimension(self) -> Dimension:
        """
        returns the name/dimension/axis of the explicit dimension characteristic.
        Names of explicit dimension characteristics are dimensions.
        @returns Dimension: the dimension of the explicit dimension characteristic.
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
        if isinstance(__value, TypedDimensionCharacteristic):
            return self.__dimension == __value.__dimension and self.__aspect == __value.__aspect and self.__value == __value.__value
        else:
            return False
    
    # internal methods
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, dimension: Dimension, value) -> "TypedDimensionCharacteristic":
        """
        Create a Dimension from an lxml.etree._Element.
        @param xml_element: the xml subtree from which the Dimension is created
        @param dimension: the dimension of the explicit dimension characteristic
        @param member: the member of the explicit dimension characteristic
        @returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
        @raises ValueError: if the XML element is malformed
        """
        
        # Get the dimension attribute from the xml element
        dimension_axis = xml_element.get("dimension")
        if dimension_axis is None:
            raise ValueError("Could not find dimension attribute in explicit dimension characteristic")

        dimension_aspect = BrelAspect.from_QName(QName.from_string(dimension_axis))

        return cls(dimension, value, dimension_aspect)