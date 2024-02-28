import brel


def test_qname_getters():
    report_uri = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000077/aapl-20230701_htm.xml"
    filing = brel.Filing.open(report_uri)

    # check if a fact with value = "true" is parsed correctly as a bool
    fact = filing.get_facts_by_concept_name("dei:DocumentQuarterlyReport")[0]
    assert fact._get_id() == "f-2", "Expected fact id to be 'f-2'"

    context = fact.get_context()
    assert context._get_id() == "c-1", "Expected context id to be 'c-1'"

    assert fact.get_value_as_str() == "true", "Expected 'true' as fact value is 'true'"
    assert fact.get_value_as_bool() == True, "Expected True as fact value is 'true'"
    try:
        fact.get_value_as_int()
        assert False, "Expected ValueError as fact value is not an integer"
    except ValueError:
        pass

    try:
        fact.get_value_as_float()
        assert False, "Expected ValueError as fact value is not a float"
    except ValueError:
        pass

    assert fact.get_unit() == None, "Expected None as fact unit is not defined"
    assert (
        str(fact.get_period()) == "from 2022-09-25 to 2023-07-01"
    ), "Expected 'from 2022-09-25 to 2023-07-01' as fact unit is 'from 2022-09-25 to 2023-07-01'"
    assert (
        str(fact.get_concept()) == "dei:DocumentQuarterlyReport"
    ), "Expected 'dei:DocumentQuarterlyReport' as fact concept is 'dei:DocumentQuarterlyReport'"
    assert "320193" in str(fact.get_entity()), "Expected '320193' to be in fact entity string"

    fact_str = str(fact)
    assert "concept" in fact_str, "Expected 'concept' to be in fact string"
    assert "period" in fact_str, "Expected 'period' to be in fact string"
    assert "entity" in fact_str, "Expected 'entity' to be in fact string"
    assert "unit" not in fact_str, "Expected 'unit' not to be in fact string"

    # check if parsing a false fact as bool works
    fact = filing.get_facts_by_concept_name("dei:AmendmentFlag")[0]
    assert fact.get_value_as_str() == "false", "Expected 'false' as fact value is 'false'"
    assert fact.get_value_as_bool() == False, "Expected False as fact value is 'false'"

    # check for an integer fact
    fact = filing.get_facts_by_concept_name("us-gaap:GrossProfit")[0]

    assert isinstance(fact.get_value_as_int(), int), "Expected int as fact value is int"
    assert fact.get_value_as_int() > 1000000, "Expected apples gross profit to be > 1M"
    assert isinstance(fact.get_value_as_float(), float), "Expected float as fact value is float"
    assert fact.get_value_as_float() > 1000000, "Expected apples gross profit to be > 1M"
    try:  # check if parsing a false fact as bool works
        fact.get_value_as_bool()
        assert False, "Expected ValueError as fact value is not a bool"
    except ValueError:
        pass
