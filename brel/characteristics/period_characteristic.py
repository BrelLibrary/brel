import lxml
import lxml.etree

from brel import QName
from brel.characteristics import Aspect, ICharacteristic

class PeriodCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL period characteristic.
    Associates the aspect Aspect.PERIOD with a value.
    The value can be an instant or a duration.
    """
    # TODO: currently the value is a string, but it should be a datetime or at least check if the string is a valid date/datetime
    # TODO: docstrings

    def __init__(self) -> None:
        self.__is_instant: bool = False
        self.instant_date: str|None = None
        self.start_date: str|None = None
        self.end_date: str|None = None
    
    # first class citizens
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
    
    def get_value(self) -> 'PeriodCharacteristic':
        return self
    
    def get_aspect(self) -> Aspect:
        return Aspect.PERIOD

    def __str__(self) -> str:
        if self.__is_instant:
            return f"on {self.instant_date}"
        else:
            return f"from {self.start_date} to {self.end_date}"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PeriodCharacteristic):
            return False
        else:
            return str(self) == str(__value)
    
    # Internal methods
    @classmethod
    def instant(cls, instant_date: str) -> "PeriodCharacteristic":
        """
        Create an instant Period.
        @param instant_date: the date of the instant
        @returns PeriodCharacteristic: the instant PeriodCharacteristic
        """
        period_instance = cls()
        period_instance.instant_date = instant_date
        period_instance.__is_instant = True

        return period_instance
    
    @classmethod
    def duration(cls, start_date: str, end_date: str) -> "PeriodCharacteristic":
        """
        Create a duration Period.
        @param start_date: the start date of the duration
        @param end_date: the end date of the duration
        @returns PeriodCharacteristic: the duration PeriodCharacteristic
        """
        period_instance = cls()
        period_instance.start_date = start_date
        period_instance.end_date = end_date
        period_instance.__is_instant = False

        return period_instance

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PeriodCharacteristic":
        """
        Create a Period from an lxml.etree._Element.
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
    