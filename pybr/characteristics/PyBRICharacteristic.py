from abc import ABC, abstractmethod
from pybr import PyBRAspect

class PyBRICharacteristic(ABC):
    @abstractmethod
    def get_value():
        raise NotImplementedError
    
    @abstractmethod
    def get_aspect() -> PyBRAspect:
        raise NotImplementedError