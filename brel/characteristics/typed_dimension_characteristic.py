"""
This module contains the class for  the typed dimension characteristic in Brel.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 19 December 2023

====================
"""

from brel.characteristics import Aspect, ICharacteristic
from brel.reportelements import Dimension, Member


class TypedDimensionCharacteristic(ICharacteristic):
    """
    Class for representing a typed dimension characteristic.
    A typed dimension characteristic assigns a dimension aspect a value.
    In Brel, the type of the value is omitted and the value is always a string.
    """

    def __init__(self, dimension: Dimension, value: str, aspect: Aspect) -> None:
        self.__dimension: Dimension = dimension
        self.__value: str = value
        self.__aspect: Aspect = aspect

    # first class citizens
    def get_aspect(self) -> Aspect:
        """
        Info: Both typed and explicit dimension characteristics are not core characteristics and therefore not available as attributes of the `Aspect` class.
        :returns Aspect: the aspect of the explicit dimension characteristic.
        """
        return self.__aspect

    def get_value(self) -> str:
        """
        :returns str: the value of the typed dimension characteristic as a string.
        """
        return self.__value

    def get_dimension(self) -> Dimension:
        """
        Info: this is not the same as calling `get_aspect()`.
        :returns Dimension: the dimension of the typed dimension characteristic.
        """
        return self.__dimension

    # second class citizens
    def __str__(self) -> str:
        return self.__value.__str__()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TypedDimensionCharacteristic):
            return (
                self.__dimension == __value.__dimension
                and self.__aspect == __value.__aspect
                and self.__value == __value.__value
            )
        else:
            return False
