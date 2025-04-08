from brel.reportelements.i_report_element import IReportElement
from brel.reportelements.abstract import Abstract
from brel.reportelements.concept import Concept
from brel.reportelements.dimension import Dimension
from brel.reportelements.hypercube import Hypercube
from brel.reportelements.lineitems import LineItems
from brel.reportelements.member import Member
from brel.qname import QName
from abc import ABC, abstractmethod


class ReportElementRepository(ABC):
    @abstractmethod
    def has_report_element(self, qname: QName) -> bool:
        """
        Check if the report element exists in the repository.
        :param qname: The QName of the report element.
        :return: True if the report element exists, False otherwise.
        """
        pass

    @abstractmethod
    def get_report_element(self, qname: QName) -> IReportElement:
        """
        Get the report element by its QName.
        :param qname: The QName of the report element.
        :return: The report element.
        """
        pass

    @abstractmethod
    def set_report_element(self, qname: QName, report_element: IReportElement) -> None:
        """
        Set the report element by its QName.
        :param qname: The QName of the report element.
        :param report_element: The report element to set.
        """
        pass
