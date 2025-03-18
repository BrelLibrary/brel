from brel.characteristics import PeriodCharacteristic
import datetime


def test_instant():
    # try to make an instant period with invalid date
    try:
        PeriodCharacteristic._instant("abc")
        assert False, "Expected ValueError as date is invalid"
    except ValueError:
        pass

    # try to make an instant period with valid date
    instant = PeriodCharacteristic._instant("2022-09-25")

    assert "2022-09-25" in str(instant), "Expected '2022-09-25' to be in period string"

    # check if the period is an instant period
    assert instant.is_instant(), "Expected period to be an instant period"

    # check if the date is correct
    assert instant.get_instant_period() == datetime.date(2022, 9, 25), "Expected date to be 2022-09-25"

    # try to get start and end date from an instant period
    # this should raise a ValueError
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
    # try to make an duration period with invalid start date
    try:
        PeriodCharacteristic._duration("abc", "2023-07-01")
        assert False, "Expected ValueError as start date is invalid"
    except ValueError:
        pass

    # try to make an duration period with invalid end date
    try:
        PeriodCharacteristic._duration("2022-09-25", "abc")
        assert False, "Expected ValueError as end date is invalid"
    except ValueError:
        pass

    # try to make a duration with end date before start date
    try:
        PeriodCharacteristic._duration("2023-10-01", "2022-09-25")
        assert False, "Expected ValueError as end date is before start date"
    except ValueError:
        pass

    # try to make a duration period with valid start and end date
    duration = PeriodCharacteristic._duration("2022-09-25", "2023-07-01")

    # check if the period is a duration period
    assert not duration.is_instant(), "Expected period to be a duration period"

    # try to get start and end date from a duration period
    # check if the dates are correct
    assert duration.get_start_period() == datetime.date(2022, 9, 25), "Expected start date to be 2022-09-25"

    assert duration.get_end_period() == datetime.date(2023, 7, 1), "Expected end date to be 2023-07-01"

    # try to get instant date from a duration period
    # this should raise a ValueError
    try:
        duration.get_instant_period()
        assert False, "Expected ValueError as period is not an instant period"
    except ValueError:
        pass


def test_period_eq():
    instant = PeriodCharacteristic._instant("2022-09-25")
    duration = PeriodCharacteristic._duration("2022-09-25", "2023-07-01")

    assert "2022-09-25" in str(duration), "Expected '2022-09-25' to be in period string"
    assert "2023-07-01" in str(duration), "Expected '2023-07-01' to be in period string"

    assert instant != duration, "Expected instant and duration to be different"
    assert instant == instant, "Expected instant to be equal to itself"
    assert duration == duration, "Expected duration to be equal to itself"
    assert duration != 123, "Expected duration to be different from 123"
