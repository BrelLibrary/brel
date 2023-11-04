import lxml
import lxml.etree

from pybr import QName, PyBRLabel
from pybr.reportelements import IReportElement

class PyBRConcept(IReportElement):
    # TODO: docstrings
    # TODO: check if the balance type, period type and balance type can be strings
    def __init__(self, name: QName, labels: list[PyBRLabel], period_type: str, balance_type: str | None, nillable: bool, data_type: str) -> None:
        self.__name: QName = name
        self.__labels: list[PyBRLabel] = labels
        self.__period_type: str = period_type
        self.__balance_type: str | None = balance_type
        self.__nillable: bool = nillable
        self.__data_type: str = data_type
        
    def get_name(self) -> QName:
        """
        Get the name of the concept.
        @return: QName containing the name of the concept
        """
        return self.__name

    def get_labels(self) -> list[PyBRLabel]:
        """
        Get the labels of the concept.
        @return: list[PyBRLabel] containing the labels of the concept
        """
        return self.__labels
    
    def add_label(self, label: PyBRLabel) -> None:
        """
        Add a label to the concept.
        @param label: the label to add to the concept
        """
        self.__labels.append(label)
    
    def get_period_type(self) -> str:
        """
        Get the period type of the concept.
        @return: str containing the period type of the concept
        """
        return self.__period_type
    
    def get_data_type(self) -> str:
        """
        Get the data type of the concept.
        @return: str containing the data type of the concept
        """
        return self.__data_type
        
    
    def get_balance_type(self) -> str | None:
        """
        Get the balance type of the concept.
        @return: str containing the balance type of the concept
        """
        return self.__balance_type
    
    def is_nillable(self) -> bool:
        """
        Check if the concept is nillable.
        @return: True 'IFF' the concept is nillable, False otherwise
        """
        return self.__nillable        
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, concept_qname: QName, labels: list[PyBRLabel]) -> "PyBRConcept":
        """
        Create a PyBRConcept from an lxml.etree._Element.
        @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the PyBRConcept from.
        @param concept_qname: QName. The QName of the concept.
        @return: PyBRConcept. The PyBRConcept created from the lxml.etree._Element.
        """
        nsmap = xml_element.nsmap

        # get the period type of the concept
        period_type = xml_element.get("{" + nsmap["xbrli"] + "}periodType", None)
        possible_period_types = ["instant", "duration"]
        if period_type not in possible_period_types:
            # raise Exception(f"Concept {concept_qname}:Unknown period type: {period_type}")
            print(f"Concept {concept_qname}:Unknown period type: {period_type}")
            period_type = None

        
        # get the balance type of the concept
        balance_type = xml_element.get("{" + nsmap["xbrli"] + "}balance", None)
        possible_balance_types = ["credit", "debit", None]  # None is for non-monetary items
        if balance_type not in possible_balance_types:
            raise Exception(f"Concept {concept_qname}:Unknown balance type: {balance_type}")
        
        
        # get if the concept is nillable
        nillable = xml_element.get("nillable", None)
        possible_nillable_values = ["true", "false"]
        if nillable not in possible_nillable_values:
            raise Exception(f"Concept {concept_qname}: Unknown nillable value: {nillable}")
        else:
            nillable = nillable == "true"
        
        # get the data type of the concept
        data_type = xml_element.get("type", None)
        if data_type is None:
            raise Exception(f"Concept {concept_qname}:No data type found for concept. every (non-abstract) concept must have a data type")
        

        return cls(concept_qname, labels, period_type, balance_type, nillable, data_type)
    
    def __str__(self) -> str:
        return self.__name.__str__()
