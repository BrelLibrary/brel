from pybr import QName, BrelLabel
from pybr.reportelements import IReportElement

class PyBRMember(IReportElement):
    def __init__(self, name: QName, labels: list[BrelLabel]):
        self.__name = name
        self.__labels = labels 
    
    def get_name(self) -> QName:
        # TODO: write docstring
        return self.__name
    
    def get_labels(self) -> list[BrelLabel]:
        # TODO: write docstring
        return self.__labels
    
    def add_label(self, label: BrelLabel):
        # TODO: write docstring
        self.__labels.append(label)
    
    def __str__(self) -> str:
        return self.__name.__str__()