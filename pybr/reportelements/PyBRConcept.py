import lxml
import lxml.etree

from pybr.reportelements import IReportElement
from pybr import PyBRLabel, QName

class PyBRConcept(IReportElement):
    def __init__(self, name: QName, labels: list[PyBRLabel]) -> None:
        self.__name = name
        self.__labels = labels
        
    def get_name(self) -> QName:
        # TODO: write docstring
        return self.__name

    def get_labels(self) -> list[PyBRLabel]:
        # TODO: write docstrig
        return self.__labels
    
    def add_label(self, label: PyBRLabel):
        # TODO: write docstring
        self.__labels.append(label)
    
    def get_period_type(self):
        # TODO: implement
        raise NotImplementedError
    
    def get_data_type(self):
        # TODO: implement
        raise NotImplementedError
    
    def get_balance_type(self):
        # TODO: implement
        raise NotImplementedError
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, concept_qname: QName) -> "PyBRConcept":
        """
        Create a PyBRConcept from an lxml.etree._Element.
        """
        # TODO: test this
        return cls(concept_qname, [])
    
    def __str__(self) -> str:
        return self.__name.__str__()
