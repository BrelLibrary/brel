"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 10 April 2025

====================
"""

from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.reportelements.i_report_element import IReportElement
from brel.qname import QName


class InMemoryReportElementRepository(ReportElementRepository):
    def __init__(self) -> None:
        self.__elements_by_qname: dict[QName, IReportElement] = {}
        self.__elemenets_by_id: dict[str, IReportElement] = {}

    def has_qname(self, qname: QName) -> bool:
        return qname in self.__elements_by_qname

    def has_id(self, id: str) -> bool:
        return id in self.__elemenets_by_id

    def get_by_qname(self, qname: QName) -> IReportElement:
        if not self.has_qname(qname):
            raise KeyError(
                f"Report element with QName {qname} not found in repository."
            )
        return self.__elements_by_qname[qname]

    def get_by_id(self, id: str) -> IReportElement:
        if not self.has_id(id):
            raise KeyError(f"Report element with ID {id} not found in repository.")
        return self.__elemenets_by_id[id]

    def upsert(self, report_element: IReportElement) -> None:
        self.__elements_by_qname[report_element.get_name()] = report_element
        report_element_id = report_element.get_id()
        if report_element_id is not None:
            self.__elemenets_by_id[report_element_id] = report_element

    def get_all(self) -> list[IReportElement]:
        return list(self.__elements_by_qname.values())
