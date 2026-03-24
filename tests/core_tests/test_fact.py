"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""

import brel
import json


def test_qname_getters():
    report_uri = "https://raw.githubusercontent.com/BrelLibrary/testfilesmirror/refs/heads/main/aapl-20230701_htm.xml"
    filing = brel.Filing.open(report_uri)

    # check if a fact with value = "true" is parsed correctly as a bool
    fact = filing.get_facts_by_concept_name("dei:DocumentQuarterlyReport")[0]
    assert fact.get_id() == "f-2", "Expected fact id to be 'f-2'"  # type: ignore

    context = fact.get_context()
    assert context._get_id() == "c-1", "Expected context id to be 'c-1'"  # type: ignore

    assert str(fact) == "true", "Expected 'true' as fact value is 'true'"
    assert bool(fact) == True, "Expected True as fact value is 'true'"
    try:
        int(fact)
        assert False, "Expected ValueError as fact value is not an integer"
    except ValueError:
        pass

    try:
        float(fact)
        assert False, "Expected ValueError as fact value is not a float"
    except ValueError:
        pass

    assert fact.get_unit() == None, "Expected None as fact unit is not defined"
    assert (
        str(fact.get_period()) == "2022-09-25/2023-07-01"
    ), "Expected '2022-09-25/2023-07-01' as fact unit is 'from 2022-09-25 to 2023-07-01'"
    assert (
        str(fact.get_concept()) == "dei:DocumentQuarterlyReport"
    ), "Expected 'dei:DocumentQuarterlyReport' as fact concept is 'dei:DocumentQuarterlyReport'"
    assert "320193" in str(
        fact.get_entity()
    ), "Expected '320193' to be in fact entity string"

    fact_str = json.dumps(dict(fact))
    assert "concept" in fact_str, "Expected 'concept' to be in fact dict"
    assert "period" in fact_str, "Expected 'period' to be in fact dict"
    assert "entity" in fact_str, "Expected 'entity' to be in fact dict"
    assert "unit" not in fact_str, "Expected 'unit' not to be in fact dict"

    # check if parsing a false fact as bool works
    fact = filing.get_facts_by_concept_name("dei:AmendmentFlag")[0]
    assert str(fact) == "false", "Expected 'false' as fact value is 'false'"
    assert bool(fact) == False, "Expected False as fact value is 'false'"

    # check for an integer fact
    fact = filing.get_facts_by_concept_name("us-gaap:GrossProfit")[0]

    assert isinstance(int(fact), int), "Expected int as fact value is int"
    assert int(fact) > 1000000, "Expected apples gross profit to be > 1M"
    assert isinstance(fact.get_value(), float), "Expected float as fact value is float"
    assert float(fact) > 1000000, "Expected apples gross profit to be > 1M"
    try:  # check if parsing a false fact as bool works
        bool(fact)
        assert False, "Expected ValueError as fact value is not a bool"
    except ValueError:
        pass


if __name__ == "__main__":
    test_qname_getters()
