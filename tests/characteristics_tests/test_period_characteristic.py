"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""


from brel.characteristics import PeriodCharacteristic
import datetime


def make_instant(date: str) -> PeriodCharacteristic:
    return PeriodCharacteristic._instant(date)  # type: ignore


def make_duration(start_date: str, end_date: str) -> PeriodCharacteristic:
    return PeriodCharacteristic._duration(start_date, end_date)  # type: ignore


def test_instant():
    try:
        make_instant("abc")
        assert False, "Expected ValueError as date is invalid"
    except ValueError:
        pass

    instant = make_instant("2022-09-25")

    assert "2022-09-25" in str(instant), "Expected '2022-09-25' to be in period string"

    assert instant.is_instant(), "Expected period to be an instant period"

    assert instant.get_instant_period() == datetime.date(
        2022, 9, 25
    ), "Expected date to be 2022-09-25"

    try:
        instant.get_start_period()
        assert False, "Expected ValueError as period is an instant period"
    except ValueError:
        pass

    try:
        instant.get_end_period()
        assert False, "Expected ValueError as period is an instant period"
    except ValueError:
        pass


def test_duration():
    try:
        make_duration("abc", "2023-07-01")
        assert False, "Expected ValueError as start date is invalid"
    except ValueError:
        pass

    try:
        make_duration("2022-09-25", "abc")
        assert False, "Expected ValueError as end date is invalid"
    except ValueError:
        pass

    try:
        make_duration("2023-10-01", "2022-09-25")
        assert False, "Expected ValueError as end date is before start date"
    except ValueError:
        pass

    duration = make_duration("2022-09-25", "2023-07-01")

    assert not duration.is_instant(), "Expected period to be a duration period"

    assert duration.get_start_period() == datetime.date(
        2022, 9, 25
    ), "Expected start date to be 2022-09-25"

    assert duration.get_end_period() == datetime.date(
        2023, 7, 1
    ), "Expected end date to be 2023-07-01"

    try:
        duration.get_instant_period()
        assert False, "Expected ValueError as period is not an instant period"
    except ValueError:
        pass


def test_period_eq():
    instant = make_instant("2022-09-25")
    duration = make_duration("2022-09-25", "2023-07-01")

    assert "2022-09-25" in str(duration), "Expected '2022-09-25' to be in period string"
    assert "2023-07-01" in str(duration), "Expected '2023-07-01' to be in period string"

    assert instant != duration, "Expected instant and duration to be different"
    assert instant == instant, "Expected instant to be equal to itself"
    assert duration == duration, "Expected duration to be equal to itself"
    assert duration != 123, "Expected duration to be different from 123"
