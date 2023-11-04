from abc import ABC, abstractmethod
from pybr.characteristics import PyBRAspect

class PyBRICharacteristic(ABC):
    """
    The Interface for a characteristic.
    A characteristic is a tuple of an aspect and a value.
    """

    @abstractmethod
    def get_value(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_aspect(self) -> PyBRAspect:
        raise NotImplementedError