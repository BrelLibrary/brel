"""
Contains the interface for a characteristic.

@author: Robin Schmidiger
@version: 0.1
@date: 2023-12-06
"""

from abc import ABC, abstractmethod
from brel.characteristics import BrelAspect

class ICharacteristic(ABC):
    """
    The Interface for a characteristic.
    A characteristic is a binding between an aspect and a value.
    """

    @abstractmethod
    def get_value(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_aspect(self) -> BrelAspect:
        raise NotImplementedError