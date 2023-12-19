"""
Contains the class for  the typed dimension characteristic in brel.

@author: Robin Schmidiger
@version: 0.4
@date: 19 December 2023
"""

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
        :info: Both typed and explicit dimension characteristics are not statically bound to an aspect.
        :returns Aspect: the aspect of the explicit dimension characteristic.
        """
        return self.__aspect
    
    def get_value(self) -> Member:
        """
        returns the value of the explicit dimension characteristic.
        Values of explicit dimension characteristics are members.
        :returns: the member of the explicit dimension characteristic.
        """
        return self.__value
    
    def get_dimension(self) -> Dimension:
        """
        returns the name/dimension/axis of the explicit dimension characteristic.
        Names of explicit dimension characteristics are dimensions.
        :returns: the dimension of the explicit dimension characteristic.
        """
        return self.__dimension
    
    # second class citizens
    def __str__(self) -> str:
        """
        returns a string representation of the explicit dimension characteristic.
        This representation is the QName of the member.
        :returns: member's QName as a str
        """
        return self.__value.__str__()
    
    def __eq__(self, __value: object) -> bool:
        """
        returns whether the explicit dimension characteristics are equal.
        Explicit dimension characteristics are equal if their dimension, member and aspect are equal.
        :returns: True if both are explicit dimension characteristics and have the same dimension, aspect and value.
        """
        if isinstance(__value, TypedDimensionCharacteristic):
            return self.__dimension == __value.__dimension and self.__aspect == __value.__aspect and self.__value == __value.__value
        else:
            return False