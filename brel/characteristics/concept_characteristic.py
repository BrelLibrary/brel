"""
====================

- author: Robin Schmidiger
- version: 0.3
- date: 12 May 2025

====================
"""

from brel.characteristics import Aspect, ICharacteristic
from brel.reportelements import Concept


class ConceptCharacteristic(ICharacteristic):
    """
    Class for representing a concept characteristic.
    The concept characteristic links the `Aspect.CONCEPT` aspect to a concept.

    """

    def __init__(self, concept: Concept) -> None:
        self.__concept: Concept = concept

    def __str__(self) -> str:
        return str(self.__concept.get_name())

    def get_value(self) -> Concept:
        """
        :returns Concept: the concept of the characteristic
        """
        return self.__concept

    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: returns the `Aspect.CONCEPT` aspect
        """
        return Aspect.CONCEPT
