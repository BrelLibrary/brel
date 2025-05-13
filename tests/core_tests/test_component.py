"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""


from brel.brel_component import Component
from brel.brel_filing import Filing
from brel.parsers.utils.optional_utils import get_or_raise


def test_component_constructor_BD():
    """
    Tests the constructor of the Component class
    """
    uri = "http://foo/role/balance"
    info = "Balance Sheet"

    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    balance_component = filing.get_component("http://foo/role/balance")
    pre_network = get_or_raise(balance_component.get_presentation_network())
    calc_network = get_or_raise(balance_component.get_calculation_network())
    hypercube_component = filing.get_component("http://foo/role/hypercube")
    def_network = get_or_raise(hypercube_component.get_definition_network())

    try:
        Component(uri, info, [pre_network, pre_network])
        assert False, "Failed to raise ValueError for multiple presentation networks"
    except ValueError as e:
        assert (
            "presentation" in str(e).lower()
        ), f"Expected ValueError for multiple presentation networks, but got {e}"

    try:
        Component(uri, info, [calc_network, calc_network])
        assert False, "Failed to raise ValueError for multiple calculation networks"
    except ValueError as e:
        assert (
            "calculation" in str(e).lower()
        ), f"Expected ValueError for multiple calculation networks, but got {e}"

    try:
        Component(uri, info, [def_network, def_network])
        assert False, "Failed to raise ValueError for multiple definition networks"
    except ValueError as e:
        assert (
            "definition" in str(e).lower()
        ), f"Expected ValueError for multiple definition networks, but got {e}"


def test_component_getters():
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    balance_component = filing.get_component("http://foo/role/balance")

    assert (
        balance_component.get_URI() == "http://foo/role/balance"
    ), f"URI is {balance_component.get_URI()}, expected http://foo/role/balance"

    assert (
        balance_component.get_info() == "Balance Sheet"
    ), f"Info is {balance_component.get_info()}, expected 'Balance Sheet'"

    pre_network = balance_component.get_presentation_network()
    assert pre_network is not None, "Balance component has no presentation network"

    calc_network = balance_component.get_calculation_network()
    assert calc_network is not None, "Balance component has no calculation network"

    def_network = balance_component.get_definition_network()
    assert def_network is None, "Balance component has a definition network"

    assert (
        balance_component.has_presentation_network()
    ), "Balance component has no presentation network"

    assert (
        balance_component.has_calculation_network()
    ), "Balance component has no calculation network"

    assert (
        not balance_component.has_definition_network()
    ), "Balance component has a definition network"

    assert balance_component.get_URI() in str(
        balance_component
    ), f"URI {balance_component.get_URI()} not in {str(balance_component)}"

    assert balance_component.get_info() in str(
        balance_component
    ), f"Info {balance_component.get_info()} not in {str(balance_component)}"

    networks = balance_component.get_networks()
    assert pre_network in networks, "Presentation network not in networks"
    assert calc_network in networks, "Calculation network not in networks"
