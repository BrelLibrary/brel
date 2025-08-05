import os
import pytest

from brel.parsers.XHMTL.xhtml_parse_facts import parse_date_fact_value, parse_numerical_fact_value
def test_parse_recurring_date_day_month_format():
    date_format = "ixt:date-day-month"
    assert parse_date_fact_value("24.04 ", date_format) == "--04-24"
    assert parse_date_fact_value("  31M12 ", date_format) == "--12-31"

    with pytest.raises(ValueError):
        parse_date_fact_value("44.10", date_format)

def test_parse_date_day_month_year_format():
    date_format = "ixt:date-day-month-year"
    assert parse_date_fact_value("24.04.2022", date_format) == "2022-04-24"
    assert parse_date_fact_value("31M12V2022", date_format) == "2022-12-31"

    with pytest.raises(ValueError):
        parse_date_fact_value("11.19.2021", date_format)

def test_parse_bulgarian_day_month_format():
    date_format = 'ixt:date-day-monthname-bg'
    assert parse_date_fact_value("24.яну", date_format) == "--01-24"
    assert parse_date_fact_value("31.май", date_format) == "--05-31"

    with pytest.raises(ValueError):
        parse_date_fact_value("31.Фев", date_format)

def test_parse_num_comma_decimal_apos():
    num_format = 'ixt:num-comma-decimal-apos'
    assert parse_numerical_fact_value("34'244,132", num_format, "0") == "34244.132"
    assert parse_numerical_fact_value("00'331,20010", num_format, "2") == "33120.01"
    assert parse_numerical_fact_value("12' 3,444", num_format, fact_scale="-4") == "0.0123444"

    with pytest.raises(ValueError):
        parse_numerical_fact_value("312..1233'312.33", num_format, fact_scale="-2.6")

if __name__ == "__main__":
    test_parse_recurring_date_day_month_format()
    test_parse_date_day_month_year_format()
    test_parse_bulgarian_day_month_format()
    test_parse_num_comma_decimal_apos()

