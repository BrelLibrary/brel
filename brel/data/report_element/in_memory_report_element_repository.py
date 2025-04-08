from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.reportelements.i_report_element import IReportElement
from brel.reportelements.abstract import Abstract
from brel.reportelements.concept import Concept
from brel.reportelements.dimension import Dimension
from brel.reportelements.hypercube import Hypercube
from brel.reportelements.lineitems import LineItems
from brel.reportelements.member import Member
from brel.qname import QName


class InMemoryReportElementRepository(ReportElementRepository):
    def __init__(self):
        self.__elements: dict[QName, IReportElement] = {}

    def has_report_element(self, qname: QName) -> bool:
        """
        Check if the report element exists in the repository.
        :param qname: The QName of the report element.
        :return: True if the report element exists, False otherwise.
        """
        return qname in self.__elements

    def get_report_element(self, qname: QName) -> IReportElement:
        """
        Get the report element by its QName.
        :param qname: The QName of the report element.
        :return: The report element.
        """
        if not self.has_report_element(qname):
            raise KeyError(f"Report element with QName {qname} not found in repository.")
        return self.__elements[qname]

    def set_report_element(self, qname: QName, report_element: IReportElement) -> None:
        """
        Set the report element by its QName.
        :param qname: The QName of the report element.
        :param report_element: The report element to set.
        """
        self.__elements[qname] = report_element
