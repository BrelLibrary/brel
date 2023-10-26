from pybr import QName, PyBRLabel

from abc import ABC, abstractmethod

class IReportElement(ABC):

    @abstractmethod
    def get_name() -> QName:
        raise NotImplementedError
    
    @abstractmethod
    def get_labels() -> list[PyBRLabel]:
        raise NotImplementedError