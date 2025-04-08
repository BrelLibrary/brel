from brel.data.report_element.in_memory_report_element_repository import InMemoryReportElementRepository
from functools import cache


@cache
def get_report_element_repository():
    return InMemoryReportElementRepository()
