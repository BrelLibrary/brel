"""
This module contains the class for representing an explicit dimension characteristic.
Explicit members are a wrapper for a dimension- and a member report element.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 2023-12-06

====================
"""

from typing import List
from brel.characteristics import Aspect, ICharacteristic
from brel.reportelements import Dimension, Member
from brel.services.translation.translation_service import TranslationService


class ExplicitDimensionCharacteristic(ICharacteristic):
    """
    Class for representing an explicit dimension characteristic.
    An explicit dimension characteristic assigns a dimension a member.

    The dimension is both a dimension report element as well as an aspect with the same QName as
    the dimension report element.

    The member is a member report element and the value of the explicit dimension characteristic.
    """

    def __init__(self, dimension: Dimension, member: Member, aspect: Aspect) -> None:
        self.__dimension = dimension
        self.__member = member
        self.__aspect = aspect

    # first class citizens
    def get_aspect(self) -> Aspect:
        """
        Info: Both typed and explicit dimension characteristics are not statically bound to an
        aspect.
        :returns Aspect: the aspect of the explicit dimension characteristic.
        """
        return self.__aspect

    def get_value(self) -> Member:
        """
        returns the value of the explicit dimension characteristic.
        Values of explicit dimension characteristics are member report elements.
        :returns Member: the member of the explicit dimension characteristic.
        """
        return self.__member

    def get_localized_value_string(
        self, languages: List[str], translation_service: TranslationService
    ) -> str:
        member = self.get_member()
        return translation_service.get_from_labels(
            member.get_labels(), languages, member.get_name().get_local_name()
        )

    def get_dimension(self) -> Dimension:
        """
        returns the name/dimension/axis of the explicit dimension characteristic.
        Names of explicit dimension characteristics are dimensions.
        This is not the same as calling `get_aspect()`.
        :returns Dimension: the dimension of the explicit dimension characteristic.
        """
        return self.__dimension

    # second class citizens
    def get_member(self) -> Member:
        """
        returns the member of the explicit dimension characteristic.
        This is equivalent to calling `get_value()`.
        :returns Member: the member of the explicit dimension characteristic.
        """
        return self.get_value()

    def __str__(self) -> str:
        return self.__member.__str__()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ExplicitDimensionCharacteristic):
            return False
        return (
            self.get_member() == __value.get_member()
            and self.get_aspect() == __value.get_aspect()
        )
