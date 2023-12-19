"""
Contains the class for representing an XBRL entity.

:author: Robin Schmidiger
:version: 0.4
:date: 19 December 2023
"""

from brel import QName
from brel.characteristics import BrelAspect, ICharacteristic
from typing import cast

class EntityCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL entity.
    An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
    Additional information about the company can be found in the entity's segment.
    """

    def __init__(self, qname: QName) -> None:
        self.__qname = qname

    # first class citizens    
    def get_aspect(self) -> BrelAspect:
        """
        returns the aspect of the entity characteristic, which is Aspect.ENTITY
        :returns: Aspect.ENTITY
        """
        return BrelAspect.ENTITY
    
    def get_value(self) -> QName:
        """
        returns the value of the entity characteristic, which is the entity's qname
        :info: the entity's qname consists of the entity's scheme and the entity's identifier
        :returns: the entity's qname
        """
        return self.__qname
    
    def get_schema(self) -> str:
        """
        :returns: the schema of the entity.
        The scheme is the url of the entity qname
        """
        return self.__qname.get_URL()
    
    def __eq__(self, __value: object) -> bool:
        """
        compares the entity characteristic to another entity characteristic
        :param __value: the entity characteristic to compare to
        :returns: True if the entity characteristics are equal, False otherwise
        """
        if not isinstance(__value, EntityCharacteristic):
            return False
        else:
            return self.__qname == __value.__qname
    
    def __str__(self) -> str:
        """
        Represents the entity characteristic as a string
        :returns: the entity characteristic's qname as a string. It is the entity scheme and the entity identifier
        """
        return self.__qname.__str__()