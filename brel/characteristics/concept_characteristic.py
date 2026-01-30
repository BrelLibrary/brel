"""
====================

- author: Robin Schmidiger
- version: 0.3
- date: 12 May 2025

====================
"""

from typing import List
from brel.characteristics import Aspect, ICharacteristic
from brel.reportelements import Concept
from brel.services.translation.translation_service import TranslationService


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

    def get_localized_value_string(
        self, languages: List[str], translation_service: TranslationService
    ) -> str:
        return translation_service.get_from_labels(
            self.__concept.get_labels(),
            languages,
            self.__concept.get_name().get_local_name(),
        )

    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: returns the `Aspect.CONCEPT` aspect
        """
        return Aspect.CONCEPT
