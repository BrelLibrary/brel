from abc import ABC, abstractmethod
from brel.characteristics import BrelAspect

class ICharacteristic(ABC):
    """
    The Interface for a characteristic.
    A characteristic is a tuple of an aspect and a value.
    """

    @abstractmethod
    def get_value(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_aspect(self) -> BrelAspect:
        raise NotImplementedError