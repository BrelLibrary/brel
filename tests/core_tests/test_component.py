import brel
import brel.networks
import brel.utils


def test_component_constructor_BD():
    """
    Tests the constructor of the Component class
    """
    uri = "http://foo/role/balance"
    info = "Balance Sheet"

    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    balance_component = filing.get_component("http://foo/role/balance")
    pre_network = balance_component.get_presentation_network()
    calc_network = balance_component.get_calculation_network()
    hypercube_component = filing.get_component("http://foo/role/hypercube")
    def_network = hypercube_component.get_definition_network()

    # create a component 2 presentation networks
    try:
        brel.Component(uri, info, [pre_network, pre_network])
        assert False, "Failed to raise ValueError for multiple presentation networks"
    except ValueError as e:
        assert "presentation" in str(e).lower(), f"Expected ValueError for multiple presentation networks, but got {e}"

    # create a component with 2 calculation networks
    try:
        brel.Component(uri, info, [calc_network, calc_network])
        assert False, "Failed to raise ValueError for multiple calculation networks"
    except ValueError as e:
        assert "calculation" in str(e).lower(), f"Expected ValueError for multiple calculation networks, but got {e}"

    # create a component with 2 definition networks
    try:
        brel.Component(uri, info, [def_network, def_network])
        assert False, "Failed to raise ValueError for multiple definition networks"
    except ValueError as e:
        assert "definition" in str(e).lower(), f"Expected ValueError for multiple definition networks, but got {e}"


def test_component_getters():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    balance_component = filing.get_component("http://foo/role/balance")

    # check if the getters return the expected networks
    # check get_URI()
    assert (
        balance_component.get_URI() == "http://foo/role/balance"
    ), f"URI is {balance_component.get_URI()}, expected http://foo/role/balance"

    # check get_info()
    assert (
        balance_component.get_info() == "Balance Sheet"
    ), f"Info is {balance_component.get_info()}, expected 'Balance Sheet'"

    # check get_presentation_network()
    pre_network = balance_component.get_presentation_network()
    assert pre_network is not None, "Balance component has no presentation network"

    # check get_calculation_network()
    calc_network = balance_component.get_calculation_network()
    assert calc_network is not None, "Balance component has no calculation network"

    # the balance sheet does not have a definition network
    # check get_definition_network()
    def_network = balance_component.get_definition_network()
    assert def_network is None, "Balance component has a definition network"

    # check has_presentation_network()
    assert balance_component.has_presentation_network(), "Balance component has no presentation network"

    # check has_calculation_network()
    assert balance_component.has_calculation_network(), "Balance component has no calculation network"

    # check has_definition_network()
    assert not balance_component.has_definition_network(), "Balance component has a definition network"

    # check that the __str__method returns the uri and the info
    assert balance_component.get_URI() in str(
        balance_component
    ), f"URI {balance_component.get_URI()} not in {str(balance_component)}"

    assert balance_component.get_info() in str(
        balance_component
    ), f"Info {balance_component.get_info()} not in {str(balance_component)}"

    # check that the presentation and definition networks are in the get_networks() method
    networks = balance_component.get_networks()
    assert pre_network in networks, "Presentation network not in networks"
    assert calc_network in networks, "Calculation network not in networks"
