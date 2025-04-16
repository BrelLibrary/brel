from datetime import date
from brel import Filing
from brel.reportelements import *
from brel.networks import *
from typing import cast


def test_end_to_end_fact_f013():
    """
    Tests the fact f-013 of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    fact = next((fact for fact in filing.get_all_facts() if fact.get_id() == "f-013"))
    fact_concept = fact.get_concept()
    fact_period = fact.get_period()
    fact_unit = fact.get_unit()
    dimension_aspect = next(
        aspect for aspect in fact.get_aspects() if not aspect.is_core()
    )
    fact_dimension = fact.get_characteristic(dimension_aspect)

    # check that the concept is ete:balance, the period is duration and the entity is 1234
    assert fact_concept.get_value() == filing.get_concept("ete:concept1")
    assert fact_period is not None
    assert fact_period.is_instant() is True
    assert fact_period.get_instant_period() == date(2024, 5, 3)
    assert fact_unit is not None
    assert fact_unit.get_value() == "USD"
    assert dimension_aspect.get_name() == "ete:additional_explicit_dimension"
    assert fact_dimension is not None
    fact_dimension_value = fact_dimension.get_value()
    assert isinstance(fact_dimension_value, Member)
    assert fact_dimension_value.get_name().get_local_name() == "foo_member"


def test_end_to_end_calculation():
    """
    Tests the calculation network of the end-to-end filing
    """

    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    components = filing.get_all_components()
    calculation_networks = [
        component.get_calculation_network()
        for component in components
        if component.get_calculation_network() is not None
    ]

    # check that there are exactly 2 calculation networks
    assert (
        len(calculation_networks) == 2
    ), f"Expected two calculation networks, got {len(calculation_networks)}"

    calculation_network_good = cast(CalculationNetwork, calculation_networks[0])
    calculation_network_bad = cast(CalculationNetwork, calculation_networks[1])

    # check that the good network is balance consistent
    assert (
        calculation_network_good.is_balance_consistent()
    ), "Good calculation network is not balance consistent"

    # check that the good network is aggregation consistent
    facts = filing.get_all_facts()
    assert calculation_network_good.is_aggregation_consistent(
        facts
    ), "Good calculation network is not aggregation consistent"

    # check that the bad network is not balance consistent
    assert (
        not calculation_network_bad.is_balance_consistent()
    ), "Bad calculation network is balance consistent"

    # check that the bad network is not aggregation consistent
    assert not calculation_network_bad.is_aggregation_consistent(
        facts
    ), "Bad calculation network is aggregation consistent"


if __name__ == "__main__":
    test_end_to_end_fact_f013()
    test_end_to_end_calculation()
