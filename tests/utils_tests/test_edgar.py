from brel import Filing
from brel.utils import open_edgar


def test_edgar_aapl_date_GD():
    aapl_cik = "320193"
    filing_type = "10-Q"
    date = "2023-12-30"

    try:
        f = open_edgar(aapl_cik, filing_type, date)
        assert isinstance(f, Filing), f"Failed to open filing: should be Filing, but is {type(f)}"
        apple_city_facts = f.get_facts_by_concept_name("dei:EntityAddressCityOrTown")
        assert len(apple_city_facts) == 1, f"Expected 1 fact, but got {len(apple_city_facts)}"
        assert (
            apple_city_facts[0].get_value() == "Cupertino"
        ), f"Expected Cupertino, but got {apple_city_facts[0].get_value()}"
    except ValueError as e:
        assert False, f"Failed to open filing: {e}"


def test_edgar_aapl_GD():
    aapl_cik = "320193"
    filing_type = "10-K"

    try:
        filing = open_edgar(aapl_cik, filing_type)
    except ValueError as e:
        assert False, f"Failed to open filing: {e}"


def test_edgar_input_BD():
    # try with a date that is not "YYYY-MM-DD"
    cik = "320193"
    filing_type = "10-K"
    date = "123-12-12"
    try:
        open_edgar(cik, filing_type, date)
        assert (
            False
        ), "Failed to raise ValueError for incorrect date format. The date has to be in the format YYYY-MM-DD, but YYY-MM-DD was given."
    except ValueError as e:
        assert "date" in str(e).lower(), f"Expected ValueError for incorrect date format, but got {e}"

    # try with a date that is not a string
    date = 123
    try:
        open_edgar(cik, filing_type, date)
        assert (
            False
        ), "Failed to raise ValueError for incorrect date format. The date has to be in the format YYYY-MM-DD, but YYY-MM-DD was given."
    except ValueError as e:
        assert "date" in str(e).lower(), f"Expected ValueError for incorrect date format, but got {e}"

    # check if the cik is too long
    date = None
    cik = "1234567891011"
    try:
        open_edgar(cik, filing_type)
        assert (
            False
        ), "Failed to raise ValueError for incorrect cik format. The cik has to be a string with 10 digits, but 13 digits were given."
    except ValueError as e:
        assert "cik" in str(e).lower(), f"Expected ValueError for incorrect cik format, but got {e}"

    # check if cik is not a str
    cik = 1234567891
    try:
        open_edgar(cik, filing_type)
        assert (
            False
        ), "Failed to raise ValueError for incorrect cik format. The cik has to be a string with 10 digits, but 10 was given."
    except ValueError as e:
        assert "cik" in str(e).lower(), f"Expected ValueError for incorrect cik format, but got {e}"

    # check if the filing type is not supported
    cik = "320193"
    filing_type = "10-Z"
    try:
        open_edgar(cik, filing_type)
        assert (
            False
        ), "Failed to raise ValueError for incorrect filing type. The filing type has to be either 10-K or 10-Q, but 10-Z was given."
    except ValueError as e:
        assert "filing type" in str(e).lower(), f"Expected ValueError for incorrect filing type, but got {e}"


def test_edgar_BD():
    # check if the cik does not exist
    cik = "0000000000"
    filing_type = "10-K"
    try:
        open_edgar(cik, filing_type)
        assert False, "Failed to raise ValueError for incorrect cik. The cik does not exist, but 0000000000 was given."
    except ValueError as e:
        assert "cik" in str(e).lower(), f"Expected ValueError for incorrect cik, but got {e}"
