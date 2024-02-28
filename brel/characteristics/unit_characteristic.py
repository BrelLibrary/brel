"""
This module contains the class for representing xbrl unit characteristics.
A unit characteristic associates the aspect Aspect.UNIT with a value.
In case of the UnitCharacteristic class, the value is a string.

However, the UnitCharacteristic can also handle more complex units consisting of numerators and denominators.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 07 January 2024

====================
"""

from brel import QName
from brel.characteristics import Aspect, ICharacteristic


class UnitCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL unit characteristic.
    A unit characteristic associates the aspect Aspect.UNIT with a value and implements the ICharacteristic interface.

    A unit can be identified by its name, which usually indicates how the unit is composed.

    Examples: "usd", "sharesPerUSD", "shares"

    A unit consists of numerators and denominators, which are lists of QNames.

    Most units are simple and consist of a single QName.
    You can use the `is_simple()` method to check if the unit is simple.

    You can get the numerators and denominators of the unit using the `get_numerators()` and `get_denominators()` methods respectively.

    The unit characteristic does have a connection to the concept characteristic.
    Namely, if the concept characteristic's concept is a monetary concept, the unit's numerators and denominators must be defined in the iso4217 namespace.
    """

    def __init__(self, name: str, numerators: list[QName], denominators: list[QName]) -> None:
        self.__name: str = name
        self.__numerators = numerators
        self.__denominators = denominators

    # first class citizens
    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: returns Aspect.UNIT
        """
        return Aspect.UNIT

    def get_numerators(self) -> list[QName]:
        """
        :returns list[QName]: all numerators of the unit
        """
        return self.__numerators

    def get_denominators(self) -> list[QName]:
        """
        :returns list[QName]: all denominators of the unit
        """
        return self.__denominators

    def get_value(self) -> str:
        """
        info: this is different from the numerators/denominators of the unit. It is the name of the unit.
        :returns str: the name of the unit
        """
        return self.__name

    # second class citizens
    def __str__(self) -> str:
        return self.get_value()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, UnitCharacteristic):
            return False

        return self.__name == __value.__name

    def is_simple(self) -> bool:
        """
        A unit is simple if it has exactly one numerator and no denominators
        :returns bool: True 'IFF' the unit is simple, False otherwise
        """
        return len(self.__numerators) == 1 and len(self.__denominators) == 0
