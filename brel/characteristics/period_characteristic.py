"""
This module contains the PeriodCharacteristic class, which represents an XBRL period characteristic.
A period characteristic associates the aspect Aspect.PERIOD with a value.
This value can be an instant or a duration.

An instant consists of a single `datetime.date` instance.

A duration consists of two `datetime.date` instances, a start date and an end date.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 08 Jan 2024

====================
"""

import dateutil.parser
import datetime

from brel.characteristics import Aspect, ICharacteristic


class PeriodCharacteristic(ICharacteristic):
    """
    Class for representing an XBRL period characteristic.
    A period characteristic is either a duration or an instant.
    Use the `is_instant()` method to check if the period is an instant or a duration.

    If the period is an instant, use the `get_instant_period()` method to get the instant date as a `datetime.date` instance.

    if the period is a duration, use the `get_start_period()` and `get_end_period()` methods to get the start and end dates as `datetime.date` instances.

    A quirk of the `PeriodCharacteristic.get_value()` method is that it returns the period characteristic itself.

    This is because the standard python package `datetime` does not have a class for representing a period as specified by XBRL.
    """

    def __init__(self) -> None:
        self.__is_instant: bool = False
        self.instant_date: datetime.date | None = None
        self.start_date: datetime.date | None = None
        self.end_date: datetime.date | None = None

    # first class citizens
    def is_instant(self) -> bool:
        """
        :returns bool: True if the period is an instant, False otherwise
        """
        return self.__is_instant

    def get_start_period(self) -> datetime.date:
        """
        :returns datetime.date: the start date of the period as a `datetime.date` instance.
        :raises ValueError: if the period is an instant. Use 'is_instant' to check if the period is an instant.
        """
        if self.start_date:
            return self.start_date
        else:
            raise ValueError(
                "Period is an instant. use 'is_instant' to check if the period is an instant."
            )

    def get_end_period(self) -> datetime.date:
        """
        :returns datetime.date: the end date of the period as a `datetime.date` instance.
        :raises ValueError: if the period is an instant. Use 'is_instant' to check if the period is an instant.
        """
        if self.end_date:
            return self.end_date
        else:
            raise ValueError(
                "Period is an instant. use 'is_instant' to check if the period is an instant."
            )

    def get_instant_period(self) -> datetime.date:
        """
        :returns datetime.date: the instant date of the period as a `datetime.date` instance.
        :raises ValueError: if the period is a duration. Use 'is_instant' to check if the period is an instant.
        """
        if self.instant_date:
            return self.instant_date
        else:
            raise ValueError(
                "Period is a duration. use 'is_instant' to check if the period is an instant."
            )

    def get_value(self) -> "PeriodCharacteristic":
        """
        :returns PeriodCharacteristic: the period characteristic itself
        """
        return self

    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: the aspect of the period characteristic, which is `Aspect.PERIOD`
        """
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
    @staticmethod
    def _is_date(date: str) -> bool:
        """
        Checks if a string is a valid date.
        :param date: the string to check
        :returns bool: True if the string is a valid date, False otherwise
        """
        try:
            dateutil.parser.parse(date)
            return True
        except ValueError:
            return False

    @classmethod
    def _instant(cls, instant_date: str) -> "PeriodCharacteristic":
        """
        Create an instant Period.
        :param instant_date: the date of the instant
        :returns PeriodCharacteristic: the instant PeriodCharacteristic
        :raises ValueError: if the instant_date is not a valid date.
        """
        if not cls._is_date(instant_date):
            raise ValueError(
                f"Instant date '{instant_date}' is not a valid date."
            )

        period_instance = cls()
        period_instance.instant_date = dateutil.parser.parse(
            instant_date
        ).date()
        period_instance.__is_instant = True

        return period_instance

    @classmethod
    def _duration(
        cls, start_date: str, end_date: str
    ) -> "PeriodCharacteristic":
        """
        Create a duration Period.
        :param start_date: the start date of the duration
        :param end_date: the end date of the duration
        :returns PeriodCharacteristic: the duration PeriodCharacteristic
        :raises ValueError: if the start_date or end_date is not a valid date.
        """
        if not cls._is_date(start_date):
            raise ValueError(f"Start date '{start_date}' is not a valid date.")

        if not cls._is_date(end_date):
            raise ValueError(f"End date '{end_date}' is not a valid date.")

        period_instance = cls()
        period_instance.start_date = dateutil.parser.parse(start_date).date()
        period_instance.end_date = dateutil.parser.parse(end_date).date()
        period_instance.__is_instant = False

        if (
            period_instance.start_date is None
            or period_instance.end_date is None
        ):
            raise ValueError(
                f"Start date '{start_date}' or end date '{end_date}' is None."
            )

        # if period_instance.start_date > period_instance.end_date:
        if period_instance.end_date < period_instance.start_date:
            raise ValueError(
                f"Start date '{start_date}' is after end date '{end_date}'"
            )

        return period_instance
