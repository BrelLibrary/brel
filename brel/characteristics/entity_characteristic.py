"""
Contains the class for representing an XBRL entity.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 07 January 2024

====================
"""

from brel.characteristics import Aspect, ICharacteristic


class EntityCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL entity.
    An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
    Additional information about the company can be found in the entity's segment.
    """

    def __init__(self, entity_id: str, scheme: str) -> None:
        self.__id = entity_id
        self.__scheme = scheme

    # first class citizens
    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: returns `Aspect.ENTITY`
        """
        return Aspect.ENTITY

    def get_value(self) -> str:
        """
        returns the value of the entity characteristic,
        which is the entity's qname in clark notation

        - The url of of the QName is the scheme of the entity characteristic.
        - The local name of the QName is the id of the entity characteristic.

        Example of an entity characteristic value: {http:www.sec.gov/CIK}0000123456
        :returns str: the entity's QName in clark notation
        """
        return "{" + self.__scheme + "}" + self.__id

    def get_schema(self) -> str:
        """
        :returns str: the schema of the entity.
        """
        return self.__scheme

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, EntityCharacteristic):
            return False
        else:
            return self.get_value() == __other.get_value()

    def __str__(self) -> str:
        return self.get_value()
