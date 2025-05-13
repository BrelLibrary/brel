"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""


from brel.brel_filing import Filing
from brel.characteristics.brel_aspect import Aspect
from brel.parsers.utils.optional_utils import get_or_raise


def test_context_getters():
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")

    cash_fact = filing.get_facts_by_concept_name("ete:cash")[0]

    aspects = cash_fact.get_aspects()
    assert Aspect.CONCEPT in aspects, f"Aspect.CONCEPT not in {aspects}"
    assert Aspect.ENTITY in aspects, f"Aspect.ENTITY not in {aspects}"
    assert Aspect.PERIOD in aspects, f"Aspect.PERIOD not in {aspects}"
    assert Aspect.UNIT in aspects, f"Aspect.UNIT not in {aspects}"

    for aspect in aspects:
        characteristic = get_or_raise(cash_fact.get_characteristic(aspect))
        assert (
            characteristic.get_aspect() == aspect
        ), f"Expected {aspect}, got {characteristic.get_aspect()}"

    context = cash_fact.get_context()

    assert context.has_characteristic(Aspect.CONCEPT), "Expected True, got False"

    concept = context.get_concept()
    assert (
        concept.get_aspect() == Aspect.CONCEPT
    ), f"Expected Aspect.CONCEPT, got {concept.get_aspect()}"
    assert (
        str(concept.get_value()) == "ete:cash"
    ), f"Expected 'ete:cash', got {concept.get_value()}"

    period = get_or_raise(context.get_period())
    assert (
        period.get_aspect() == Aspect.PERIOD
    ), f"Expected Aspect.PERIOD, got {period.get_aspect()}"
    assert "2018" in str(
        period.get_value()
    ), f"Expected '2018', got {period.get_value()}"
    assert "2024" in str(
        period.get_value()
    ), f"Expected '2024', got {period.get_value()}"

    entity = get_or_raise(context.get_entity())
    assert (
        entity.get_aspect() == Aspect.ENTITY
    ), f"Expected Aspect.ENTITY, got {entity.get_aspect()}"
    assert "1234" in entity.get_value(), f"Expected '1234', got {entity.get_value()}"

    unit = get_or_raise(context.get_unit())
    assert (
        unit.get_aspect() == Aspect.UNIT
    ), f"Expected Aspect.UNIT, got {unit.get_aspect()}"
    assert "USD" in unit.get_value(), f"Expected 'USD', got {unit.get_value()}"

    assert context._get_id() == "c-001", f"Expected 'c-001', got {context._get_id()}"  # type: ignore

    assert context.__eq__(context), "Expected True, got False"

    assert "ete:cash" in str(context), f"Expected 'ete:cash', got {str(context)}"
