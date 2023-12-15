from abc import ABC, abstractmethod
from brel import QName, BrelLabel, BrelLabelRole

class IReportElement(ABC):
    # first class citizens
    @abstractmethod
    def get_name(self) -> QName:
        raise NotImplementedError
    
    @abstractmethod
    def get_labels(self) -> list[BrelLabel]:
        raise NotImplementedError
    
    @abstractmethod
    def _add_label(self, label: BrelLabel):
        raise NotImplementedError
    
    # second class citizens
    def has_label(self, label_role: BrelLabelRole) -> bool:
        return any(label.get_role() == label_role for label in self.get_labels())