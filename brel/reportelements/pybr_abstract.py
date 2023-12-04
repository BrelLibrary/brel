from brel import QName, BrelLabel
from brel.reportelements import IReportElement

class Abstract(IReportElement):
    def __init__(self, qname: QName, labels: list[BrelLabel]) -> None:
        self.__qname = qname
        self.__labels = labels
    
    def get_name(self) -> QName:
        """
        Get the name of the abstract element.
        @return: QName containing the name of the abstract element
        """        
        return self.__qname
    
    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the abstract element.
        @return: list[Label] containing the labels of the abstract element
        """
        return self.__labels
    
    def _add_label(self, label: BrelLabel):
        """
        Add a label to the abstract element.
        @param label: the label to add to the abstract element
        """
        self.__labels.append(label)
    
    def __str__(self) -> str:
        return self.__qname.__str__()
    
