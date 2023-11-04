from abc import ABC, abstractmethod
from pybr import QName, PyBRLabel

class IReportElement(ABC):

    @abstractmethod
    def get_name(self) -> QName:
        raise NotImplementedError
    
    @abstractmethod
    def get_labels(self) -> list[PyBRLabel]:
        raise NotImplementedError
    
    @abstractmethod
    def add_label(self, label: PyBRLabel):
        raise NotImplementedError