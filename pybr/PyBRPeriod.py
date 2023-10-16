import lxml
import lxml.etree
from pybr import PyBRAspect

class PyBRPeriod(PyBRAspect):
    """
    Class for representing an XBRL period.
    An XBRL period can be either instant or duration.
    If it is instant, it has an instant date.
    If it is duration, it has a start date and an end date.
    """

    def __init__(self) -> None:
        self.__is_instant: bool = False
        self.instant_date: str|None = None
        self.start_date: str|None = None
        self.end_date: str|None = None

    @classmethod
    def instant(cls, instant_date: str) -> "PyBRPeriod":
        """
        Create an instant PyBRPeriod.
        """
        period_instance = cls()
        period_instance.instant_date = instant_date
        period_instance.__is_instant = True

        return period_instance
    
    @classmethod
    def duration(cls, start_date: str, end_date: str) -> "PyBRPeriod":
        """
        Create a duration PyBRPeriod.
        """
        period_instance = cls()
        period_instance.start_date = start_date
        period_instance.end_date = end_date
        period_instance.__is_instant = False

        return period_instance

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRPeriod":
        """
        Create a PyBRPeriod from an lxml.etree._Element.
        """
        is_instant = xml_element.find("{*}instant") is not None
        if is_instant:
            instant_date = xml_element.find("{*}instant").text
            return cls.instant(instant_date)
        else:
            start_date = xml_element.find("{*}startDate").text
            end_date = xml_element.find("{*}endDate").text
            return cls.duration(start_date, end_date)
    
    def __str__(self) -> str:
        if self.__is_instant:
            return f"on {self.instant_date}"
        else:
            return f"from {self.start_date} to {self.end_date}"
    
    def is_instant(self) -> bool:
        return self.__is_instant
    
    def get_start_period(self) -> str:
        if self.start_date:
            return self.start_date
        else:
            return ""
    
    def get_end_period(self) -> str:
        if self.end_date:
            return self.end_date
        else:
            return ""
    
    def get_instant_period(self) -> str:
        if self.instant_date:
            return self.instant_date
        else:
            return ""
    
    def get_name(self) -> str:
        return self.__str__()