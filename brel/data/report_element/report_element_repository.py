"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 15 April 2025

====================
"""

from brel.reportelements.i_report_element import IReportElement
from brel.qname import QName
from abc import ABC, abstractmethod


class ReportElementRepository(ABC):
    @abstractmethod
    def has_qname(self, qname: QName) -> bool:
        pass

    @abstractmethod
    def has_id(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_qname(self, qname: QName) -> IReportElement:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> IReportElement:
        pass

    @abstractmethod
    def upsert(self, report_element: IReportElement) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[IReportElement]:
        pass

    def get_typed_by_qname[
        T: IReportElement
    ](self, qname: QName, report_element_type: type[T]) -> T:
        report_element = self.get_by_qname(qname)
        if not isinstance(report_element, report_element_type):
            raise ValueError(
                f"Report element {qname} is not of type {report_element_type}. It is of type {type(report_element)}"
            )
        return report_element

    def get_typed_by_id[
        T: IReportElement
    ](self, id: str, report_element_type: type[T]) -> T:
        report_element = self.get_by_id(id)
        if not isinstance(report_element, report_element_type):
            raise ValueError(
                f"Report element {id} is not of type {report_element_type}. It is of type {type(report_element)}"
            )
        return report_element

    def has_typed_qname(
        self, qname: QName, report_element_type: type[IReportElement]
    ) -> bool:
        try:
            self.get_typed_by_qname(qname, report_element_type)
            return True
        except ValueError:
            return False

    def has_typed_id(self, id: str, report_element_type: type[IReportElement]) -> bool:
        """
        Check if the report element exists in the repository.
        :param id: The ID of the report element.
        :param type: The type of the report element.
        :return: True if the report element exists, False otherwise.
        """
        try:
            self.get_typed_by_id(id, report_element_type)
            return True
        except ValueError:
            return False
