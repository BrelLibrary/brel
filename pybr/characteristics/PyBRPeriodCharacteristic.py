import lxml
import lxml.etree
from pybr import QName, PyBRAspect
from pybr.characteristics import PyBRICharacteristic

class PyBRPeriodCharacteristic(PyBRICharacteristic):
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
    def instant(cls, instant_date: str) -> "PyBRPeriodCharacteristic":
        """
        Create an instant PyBRPeriod.
        """
        period_instance = cls()
        period_instance.instant_date = instant_date
        period_instance.__is_instant = True

        return period_instance
    
    @classmethod
    def duration(cls, start_date: str, end_date: str) -> "PyBRPeriodCharacteristic":
        """
        Create a duration PyBRPeriod.
        """
        period_instance = cls()
        period_instance.start_date = start_date
        period_instance.end_date = end_date
        period_instance.__is_instant = False

        return period_instance

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRPeriodCharacteristic":
        """
        Create a PyBRPeriod from an lxml.etree._Element.
        """
        nsmap = QName.get_nsmap()

        is_instant = xml_element.find("{*}instant", nsmap) is not None
        if is_instant:
            instant_date = xml_element.find("{*}instant", nsmap).text
            return cls.instant(instant_date)
        else:
            start_date = xml_element.find("{*}startDate", nsmap).text
            end_date = xml_element.find("{*}endDate", nsmap).text
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
    
    def get_value(self) -> 'PyBRPeriodCharacteristic':
        # TODO: maybe change this to a datetime
        return self
    
    def get_aspect(self) -> PyBRAspect:
        return PyBRAspect.PERIOD