
from pybr import QName, PyBRLabel
from pybr.reportelements import IReportElement

class PyBRAbstract(IReportElement):
    def __init__(self, qname: QName, labels: list[PyBRLabel]) -> None:
        self.__qname = qname
        self.__labels = labels
    
    def get_name(self) -> QName:
        """
        Get the name of the abstract element.
        @return: QName containing the name of the abstract element
        """        
        return self.__qname
    
    def get_labels(self) -> list[PyBRLabel]:
        """
        Get the labels of the abstract element.
        @return: list[PyBRLabel] containing the labels of the abstract element
        """
        return self.__labels
    
    def add_label(self, label: PyBRLabel):
        """
        Add a label to the abstract element.
        @param label: the label to add to the abstract element
        """
        self.__labels.append(label)
    
    def __str__(self) -> str:
        return self.__qname.__str__()
    
