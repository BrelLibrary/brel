"""
This file contains the UnitCharacteristic class.
It is used to represent an XBRL unit in brel.

@author: Robin Schmidiger
@version: 0.2
@date: 20 December 2023
"""

from brel import QName
from brel.characteristics import BrelAspect, ICharacteristic

class UnitCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL unit.
    It consists of and some stuff that I have not implemented yet
    """
    __unit_cache: dict[QName, 'UnitCharacteristic'] = {}

    def __init__(self, name: QName, numerators: list[QName], denominators: list[QName]) -> None:
        """
        Create a Unit.
        @param name: the name of the unit given as a QName
        @param numerators: the numerators of the unit given as a list of QNames
        @param denominators: the denominators of the unit given as a list of QNames
        """

        self.__name: QName = name
        self.__numerators = numerators
        self.__denominators = denominators

        self.__unit_cache[name] = self
    
    # first class citizens
    def get_aspect(self) -> BrelAspect:
        """
        @returns Aspect: returns Aspect.UNIT
        """
        return BrelAspect.UNIT
    
    def get_numerators(self) -> list[QName]:
        """
        @returns list[QName]: the numerators of the unit
        """
        return self.__numerators
    
    def get_denominators(self) -> list[QName]:
        """
        @returns list[QName]: the denominators of the unit
        """
        return self.__denominators
    
    def get_value(self) -> QName:
        """
        @returns QName: the name of the unit
        @info: this is different from the numerators/denominators of the unit
        """
        return self.__name
    
    # second class citizens
    def __str__(self) -> str:
        """
        @returns str: the local name of the unit
        """
        # return self.__name.__str__()
        # it's probably better to just return the localname of the unit
        return self.__name.__str__()
    
    def __eq__(self, __value: object) -> bool:
        """
        @returns bool: True 'IFF' the unit is equal to the given value
        """
        if not isinstance(__value, UnitCharacteristic):
            return False
        
        return self.__name == __value.__name
    
    def is_simple(self) -> bool:
        """
        A unit is simple if it has exactly one numerator and no denominators
        @return: True 'IFF' the unit is simple, False otherwise
        """
        return len(self.__numerators) == 1 and len(self.__denominators) == 0
