import brel
from brel.characteristics import *


def test_context_getters():
    # open ete filing
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")

    # get a ete:cash fact
    cash_fact = filing.get_facts_by_concept_name("ete:cash")[0]

    # check if get_aspects() contains Aspect.CONCEPT, Aspect.ENTITY, Aspect.PERIOD, Aspect.UNIT
    aspects = cash_fact.get_aspects()
    assert Aspect.CONCEPT in aspects, f"Aspect.CONCEPT not in {aspects}"
    assert Aspect.ENTITY in aspects, f"Aspect.ENTITY not in {aspects}"
    assert Aspect.PERIOD in aspects, f"Aspect.PERIOD not in {aspects}"
    assert Aspect.UNIT in aspects, f"Aspect.UNIT not in {aspects}"

    # for all aspects, check if the get_characteristic(...).get_aspect() is the aspect
    for aspect in aspects:
        characteristic = cash_fact.get_characteristic(aspect)
        assert characteristic.get_aspect() == aspect, f"Expected {aspect}, got {characteristic.get_aspect()}"

    context = cash_fact.get_context()

    # check if has_characteristic(Aspect.CONCEPT) is True
    assert context.has_characteristic(Aspect.CONCEPT), "Expected True, got False"

    # check if get_characteristic_as_str(Aspect.CONCEPT) is "ete:cash"
    assert (
        str(context.get_characteristic_as_str(Aspect.CONCEPT)) == "ete:cash"
    ), f"Expected 'ete:cash', got {context.get_characteristic_as_str(Aspect.CONCEPT)}"

    # check if get_concept().get_aspect() is Aspect.CONCEPT
    concept = context.get_concept()
    assert concept.get_aspect() == Aspect.CONCEPT, f"Expected Aspect.CONCEPT, got {concept.get_aspect()}"
    # check if the concepts string is "ete:cash"
    assert str(concept.get_value()) == "ete:cash", f"Expected 'ete:cash', got {concept.get_value()}"

    # check if get_period().get_aspect() is Aspect.PERIOD
    period = context.get_period()
    # check if the period string contains 2018 and 2024
    assert period.get_aspect() == Aspect.PERIOD, f"Expected Aspect.PERIOD, got {period.get_aspect()}"
    assert "2018" in str(period.get_value()), f"Expected '2018', got {period.get_value()}"
    assert "2024" in str(period.get_value()), f"Expected '2024', got {period.get_value()}"

    # check for the entity
    entity = context.get_entity()
    assert entity.get_aspect() == Aspect.ENTITY, f"Expected Aspect.ENTITY, got {entity.get_aspect()}"
    # check if the entity string contains 1234
    assert "1234" in entity.get_value(), f"Expected '1234', got {entity.get_value()}"

    # check if the unit is USD
    unit = context.get_unit()
    assert unit.get_aspect() == Aspect.UNIT, f"Expected Aspect.UNIT, got {unit.get_aspect()}"
    assert "USD" in unit.get_value(), f"Expected 'USD', got {unit.get_value()}"

    # check if _get_id() returns 'c-001'
    assert context._get_id() == "c-001", f"Expected 'c-001', got {context._get_id()}"

    # check if __eq__ with itself is True
    assert context.__eq__(context), "Expected True, got False"

    # check if __str__ contains "ete:cash"
    assert "ete:cash" in str(context), f"Expected 'ete:cash', got {str(context)}"
