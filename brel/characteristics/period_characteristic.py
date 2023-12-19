import lxml
import lxml.etree
import dateutil.parser
import datetime

from brel import QName, QNameNSMap
from brel.characteristics import BrelAspect, ICharacteristic

class PeriodCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL period characteristic.
    Associates the aspect Aspect.PERIOD with a value.
    The value can be an instant or a duration.
    """
    # TODO: currently the value is a string, but it should be a datetime or at least check if the string is a valid date/datetime

    def __init__(self) -> None:
        self.__is_instant: bool = False
        self.instant_date: datetime.date|None = None
        self.start_date: datetime.date|None = None
        self.end_date: datetime.date|None = None
    
    # first class citizens
    def is_instant(self) -> bool:
        """
        @returns bool: True if the period is an instant, False otherwise
        """
        return self.__is_instant
    
    def get_start_period(self) -> datetime.date:
        """
        @returns str: the start date of the period.
        @raises ValueError: if the period is an instant. Use 'is_instant' to check if the period is an instant.
        """
        if self.start_date:
            return self.start_date
        else:
            raise ValueError("Period is an instant. use 'is_instant' to check if the period is an instant.")
    
    def get_end_period(self) -> datetime.date:
        """
        @returns str: the end date of the period.
        @raises ValueError: if the period is an instant. Use 'is_instant' to check if the period is an instant.
        """
        if self.end_date:
            return self.end_date
        else:
            raise ValueError("Period is an instant. use 'is_instant' to check if the period is an instant.")
    
    def get_instant_period(self) -> str:
        """
        @returns str: the instant date of the period.
        @raises ValueError: if the period is a duration. Use 'is_instant' to check if the period is an instant.
        """
        if self.instant_date:
            return self.instant_date
        else:
            raise ValueError("Period is a duration. use 'is_instant' to check if the period is an instant.")
    
    def get_value(self) -> 'PeriodCharacteristic':
        """
        @returns PeriodCharacteristic: the period characteristic itself
        """
        return self
    
    def get_aspect(self) -> BrelAspect:
        """
        @returns Aspect: the aspect of the period characteristic, which is Aspect.PERIOD
        """
        return BrelAspect.PERIOD

    def __str__(self) -> str:
        """
        Returns the period as a string.
        If the period is an instant, the string is 'on {instant_date}'.
        If the period is a duration, the string is 'from {start_date} to {end_date}'.
        @returns str: the period as a string
        """
        if self.__is_instant:
            return f"on {self.instant_date}"
        else:
            return f"from {self.start_date} to {self.end_date}"
    
    def __eq__(self, __value: object) -> bool:
        """
        Compares the period characteristic to another period characteristic.
        @param __value: the period characteristic to compare to
        @returns bool: True if the period characteristics are equal, False otherwise
        """
        if not isinstance(__value, PeriodCharacteristic):
            return False
        else:
            return str(self) == str(__value)
    
    # Internal methods
    @staticmethod
    def is_date(date: str) -> bool:
        """
        Checks if a string is a valid date.
        @param date: the string to check
        @returns bool: True if the string is a valid date, False otherwise
        """
        try:
            dateutil.parser.parse(date)
            return True
        except ValueError:
            return False

    @classmethod
    def instant(cls, instant_date: str) -> "PeriodCharacteristic":
        """
        Create an instant Period.
        @param instant_date: the date of the instant
        @returns PeriodCharacteristic: the instant PeriodCharacteristic
        @raises ValueError: if the instant_date is not a valid date.
        """
        if not cls.is_date(instant_date):
            raise ValueError(f"Instant date '{instant_date}' is not a valid date.")

        period_instance = cls()
        period_instance.instant_date = dateutil.parser.parse(instant_date).date()
        period_instance.__is_instant = True

        return period_instance
    
    @classmethod
    def duration(cls, start_date: str, end_date: str) -> "PeriodCharacteristic":
        """
        Create a duration Period.
        @param start_date: the start date of the duration
        @param end_date: the end date of the duration
        @returns PeriodCharacteristic: the duration PeriodCharacteristic
        @raises ValueError: if the start_date or end_date is not a valid date.
        """
        if not cls.is_date(start_date):
            raise ValueError(f"Start date '{start_date}' is not a valid date.")
        
        if not cls.is_date(end_date):
            raise ValueError(f"End date '{end_date}' is not a valid date.")


        period_instance = cls()
        period_instance.start_date = dateutil.parser.parse(start_date).date()
        period_instance.end_date = dateutil.parser.parse(end_date).date()
        period_instance.__is_instant = False

        if period_instance.start_date > period_instance.end_date:
            raise ValueError(f"Start date '{start_date}' is after end date '{end_date}'")

        return period_instance

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, qname_nsmap: QNameNSMap) -> "PeriodCharacteristic":
        """
        Create a Period from an lxml.etree._Element.
        """
        nsmap = qname_nsmap.get_nsmap()

        is_instant = xml_element.find("{*}instant", nsmap) is not None
        if is_instant:
            instant_date_elem = xml_element.find("{*}instant", nsmap)
            if instant_date_elem is None:
                raise ValueError("Could not find instant element in period characteristic")
            instant_date = instant_date_elem.text
            if instant_date is None:
                raise ValueError("The instant element has no text")
            return cls.instant(instant_date)
        else:
            start_date_elem = xml_element.find("{*}startDate", nsmap)
            if start_date_elem is None:
                raise ValueError("Could not find startDate element in period characteristic")
            start_date = start_date_elem.text
            if start_date is None:
                raise ValueError("The startDate element has no text")
            
            end_date_elem = xml_element.find("{*}endDate", nsmap)
            if end_date_elem is None:
                raise ValueError("Could not find endDate element in period characteristic")
            end_date = end_date_elem.text
            if end_date is None:
                raise ValueError("The endDate element has no text")

            return cls.duration(start_date, end_date)
    