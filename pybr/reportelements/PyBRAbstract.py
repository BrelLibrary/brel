
from pybr import QName, PyBRLabel
from pybr.reportelements import IReportElement

class PyBRAbstract(IReportElement):
    def __init__(self, qname: QName, labels: list[PyBRLabel]) -> None:
        self.__qname = qname
        self.__labels = labels
    
    def get_name(self) -> QName:
        # TODO: write docstring
        return self.__qname
    
    def get_labels(self) -> list[PyBRLabel]:
        # TODO: write docstring
        return self.__labels
    
    def add_label(self, label: PyBRLabel):
        # TODO: write docstring
        self.__labels.append(label)
    
    def __str__(self) -> str:
        return self.__qname.__str__()
    
