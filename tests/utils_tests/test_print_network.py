from brel.utils import pprint_network, pprint_network_node
import brel
import sys
from io import StringIO


def method_output_to_string(method) -> str:
    # redirect stdout to a string
    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()

    # call the method
    method()

    # get the printed string
    printed = new_stdout.getvalue()

    # reset stdout
    sys.stdout = old_stdout

    return printed


def test_print_network_roles():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    network = filing.get_component("http://foo/role/balance").get_presentation_network()

    # redirect stdout to a string
    printed_network = method_output_to_string(lambda: pprint_network(network))

    # check if the printed network is as expected
    # check if the role uri is printed
    assert "http://foo/role/balance" in printed_network, f"role: http://foo/role/balance not in {printed_network}"
    # check if 'http://www.xbrl.org/2003/arcrole/parent-child' is printed
    assert (
        "http://www.xbrl.org/2003/arcrole/parent-child" in printed_network
    ), f"arcrole: http://www.xbrl.org/2003/arcrole/parent-child not in {printed_network}"


def test_print_network_names():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    network = filing.get_component("http://foo/role/balance").get_presentation_network()

    # redirect stdout to a string
    printed_network = method_output_to_string(lambda: pprint_network(network))

    # check for the link name 'link:presentationLink'
    assert "link:presentationLink" in printed_network, f"link:presentationLink not in {printed_network}"
    # check for 'link:presentationArc'
    assert "link:presentationArc" in printed_network, f"link:presentationArc not in {printed_network}"
    # check that 'link:calculationLink' and 'link:calculationArc' are not in the printed network
    assert "link:calculationLink" not in printed_network, f"link:calculationLink in {printed_network}"
    assert "link:calculationArc" not in printed_network, f"link:calculationArc in {printed_network}"


def test_print_network_order():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    network = filing.get_component("http://foo/role/balance").get_presentation_network()
    printed_network = method_output_to_string(lambda: pprint_network(network))

    # check that the words 'Balance', 'Assets', 'Cash' and 'Liabilities' are in the printed network
    assert "balance" in printed_network, f"Balance not in {printed_network}"
    assert "assets" in printed_network, f"Assets not in {printed_network}"
    assert "cash" in printed_network, f"Cash not in {printed_network}"
    assert "liabilities" in printed_network, f"Liabilities not in {printed_network}"


def test_print_network_elements():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    network = filing.get_component("http://foo/role/balance").get_presentation_network()
    printed_network = method_output_to_string(lambda: pprint_network(network))
    # check that they are printed in the right order
    assert printed_network.index("balance") < printed_network.index(
        "assets"
    ), f"Balance not before Assets in {printed_network}"
    assert printed_network.index("assets") < printed_network.index(
        "cash"
    ), f"Assets not before Cash in {printed_network}"
    assert printed_network.index("cash") < printed_network.index(
        "liabilities"
    ), f"Cash not before Liabilities in {printed_network}"
    assert printed_network.index("balance") < printed_network.index(
        "liabilities"
    ), f"Liabilities not before Balance in {printed_network}"

    # 'Cash' is the first child of 'Assets'. therefore there should be exactly one newline between 'Assets' and 'Cash'
    characters_between_assets_and_cash = printed_network[
        printed_network.index("assets") : printed_network.index("cash")
    ]
    assert (
        characters_between_assets_and_cash.count("\n") == 1
    ), f"more than one newline between Assets and Cash in {characters_between_assets_and_cash}"

    # 'Balance' is an Abstract. therefore '[ABSTRACT]' should be printed in the same line
    # So "'Balance' -> '[ABSTRACT]'"", which is equivalent to "not 'Balance' or '[ABSTRACT]'"
    lines = printed_network.split("\n")
    assert all(
        "balance_sheet" not in line or "[ABSTRACT]" in line for line in lines
    ), f"Balance not before [ABSTRACT] in {lines}"

    # 'Cash' is a concept. therefore '[CONCEPT]' should be printed in the same line
    assert all("cash" not in line or "[CONCEPT]" in line for line in lines), f"Cash not before [CONCEPT] in {lines}"


def test_none_network():
    printed_network = method_output_to_string(lambda: pprint_network(None))
    assert printed_network == "", f"Expected empty string, got {printed_network}"

    printed_network_node = method_output_to_string(lambda: pprint_network_node(None))
    assert printed_network_node == "", f"Expected empty string, got {printed_network_node}"


def test_resource_network():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    label_network = next(
        (
            network
            for network in filing.get_all_physical_networks()
            if network.get_link_name().get_local_name() == "labelLink"
        ),
        None,
    )

    assert isinstance(label_network, brel.networks.INetwork), f"No label network found. Found {type(label_network)}"

    assert label_network is not None, "No label network found"

    printed_network = method_output_to_string(lambda: pprint_network(label_network))

    # check if '[LABEL]' occurs
    assert "[LABEL]" in printed_network, f"[LABEL] not in {printed_network}"
    # check if '[CONCEPT]' occurs
    assert "[CONCEPT]" in printed_network, f"[CONCEPT] not in {printed_network}"

    footnote_network = next(
        (
            network
            for network in filing.get_all_physical_networks()
            if network.get_link_name().get_local_name() == "footnoteLink"
        ),
        None,
    )

    assert footnote_network is not None, "No footnote network found"

    printed_network = method_output_to_string(lambda: pprint_network(footnote_network))
    # check if '[FOOTNOTE]' occurs

    assert "[FOOTNOTE]" in printed_network, f"[FOOTNOTE] not in {printed_network}"

    reference_network = next(
        (
            network
            for network in filing.get_all_physical_networks()
            if network.get_link_name().get_local_name() == "referenceLink"
        ),
        None,
    )

    assert reference_network is not None, "No reference network found"

    printed_network = method_output_to_string(lambda: pprint_network(reference_network))
    # check if '[REFERENCE]' occurs
    assert "[REFERENCE]" in printed_network, f"[REFERENCE] not in {printed_network}"


def test_print_calculation_network():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    network = filing.get_component("http://foo/role/balance").get_calculation_network()
    printed_network = method_output_to_string(lambda: pprint_network(network))

    # check if the network prints weights
    assert "[W=" in printed_network, f"Weight not in {printed_network}"

    # check if the network prints the arc role
    assert (
        "http://www.xbrl.org/2003/arcrole/summation-item" in printed_network
    ), f"arcrole: http://www.xbrl.org/2003/arcrole/summation-item not in {printed_network}"
    # check if the arc name is calculationArc
    assert "link:calculationArc" in printed_network, f"link:calculationArc not in {printed_network}"
