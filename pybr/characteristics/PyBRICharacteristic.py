from abc import ABC, abstractmethod
from pybr import PyBRAspect

class PyBRICharacteristic(ABC):
    """
    The Interface for a characteristic.
    A characteristic is a tuple of an aspect and a value.
    """

    @abstractmethod
    def get_value():
        raise NotImplementedError
    
    @abstractmethod
    def get_aspect() -> PyBRAspect:
        raise NotImplementedError