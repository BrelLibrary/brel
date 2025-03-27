from brel import Filing
from brel.resource import BrelLabel
from brel.utils import pprint
from brel.reportelements import *
from brel.networks import *
from typing import cast


def test_end_to_end_report_elements():
    """
    Tests the report elements of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/ete_filing")

    report_elements = filing.get_all_report_elements()

    print("Report elements:")
    # check the report elements
    # check that all report elements have different names
    for report_element in report_elements:
        re_name = report_element.get_name()
        if re_name.get_prefix() != "ete":
            continue
        assert (
            len([re for re in report_elements if re.get_name() == re_name]) == 1
        ), f"Duplicate report element name: {re_name}"

    # go over all report elements and check that they have the correct type
    for report_element in report_elements:
        re_local_name = report_element.get_name().get_local_name().lower()
        re_prefix = report_element.get_name().get_prefix().lower()

        if re_prefix != "ete":
            continue

        if "abstract" in re_local_name:
            assert isinstance(report_element, Abstract) or isinstance(
                report_element, LineItems
            ), f"Report element {report_element.get_name()} is not an Abstract/LineItems, but a {type(report_element)}"
        elif "dimension" in re_local_name:
            assert isinstance(
                report_element, Dimension
            ), f"Report element {report_element.get_name()} is not a Dimension, but a {type(report_element)}"
        elif "hypercube" in re_local_name:
            assert isinstance(
                report_element, Hypercube
            ), f"Report element {report_element.get_name()} is not a Hypercube, but a {type(report_element)}"
        elif "member" in re_local_name:
            assert isinstance(
                report_element, Member
            ), f"Report element {report_element.get_name()} is not a Member, but a {type(report_element)}"
        elif "lineitems" in re_local_name:
            assert isinstance(report_element, LineItems) or isinstance(
                report_element, Abstract
            ), f"Report element {report_element.get_name()} is not a LineItems/Abstract, but a {type(report_element)}"


def test_end_to_end_labels():
    """
    Tests the labels of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/ete_filing")
    report_elements = filing.get_all_report_elements()

    # go over all report elements and check that they have the correct type
    for report_element in report_elements:
        re_prefix = report_element.get_name().get_prefix().lower()

        if re_prefix != "ete":
            continue

        # check if all report elements do not have more than one label
        assert (
            len(report_element.get_labels()) <= 1
        ), f"Report element {report_element.get_name()} has more than one label"

        # check that all label roles are standard labels
        for label in report_element.get_labels():
            assert (
                label.get_label_role() == BrelLabel.STANDARD_LABEL_ROLE
            ), f"Label {label.get_content()} of report element {report_element.get_name()} has a non-standard role {label.get_label_role()}"


def test_end_to_end_components():
    """
    Tests the components of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/ete_filing")

    # check the calculation networks
    components = filing.get_all_components()
    calculation_networks = [
        component.get_calculation_network()
        for component in components
        if component.get_calculation_network() is not None
    ]

    assert len(calculation_networks) == 2, f"Expected two calculation networks, got {len(calculation_networks)}"

    # check if there are components with the uris "http://foo/role/balance" and "http://foo/role/hypercube"
    assert any(
        component.get_URI() == "http://foo/role/balance" for component in components
    ), "No component with URI 'http://foo/role/balance' found"

    assert any(
        component.get_URI() == "http://foo/role/hypercube" for component in components
    ), "No component with URI 'http://foo/role/hypercube' found"

    # check that both of them are also returned by the get_all_component_uris()
    assert (
        "http://foo/role/balance" in filing.get_all_component_uris()
    ), "URI 'http://foo/role/balance' not in get_all_component_uris()"

    assert (
        "http://foo/role/hypercube" in filing.get_all_component_uris()
    ), "URI 'http://foo/role/hypercube' not in get_all_component_uris()"

    # check that the "http://foo/role/balance" component has a calculation network and a presentation network, but no definition network
    balance_component = filing.get_component("http://foo/role/balance")
    assert balance_component.get_calculation_network() is not None, "Balance component has no calculation network"

    assert balance_component.get_presentation_network() is not None, "Balance component has no presentation network"

    assert balance_component.get_definition_network() is None, "Balance component has a definition network"


def test_end_to_end_calculation():
    """
    Tests the calculation network of the end-to-end filing
    """

    filing = Filing.open("tests/end_to_end_tests/ete_filing")
    components = filing.get_all_components()
    calculation_networks = [
        component.get_calculation_network()
        for component in components
        if component.get_calculation_network() is not None
    ]

    # check that there are exactly 2 calculation networks
    assert len(calculation_networks) == 2, f"Expected two calculation networks, got {len(calculation_networks)}"

    calculation_network_good = cast(CalculationNetwork, calculation_networks[0])
    calculation_network_bad = cast(CalculationNetwork, calculation_networks[1])

    # check that the good network is balance consistent
    assert calculation_network_good.is_balance_consistent(), "Good calculation network is not balance consistent"

    # check that the good network is aggregation consistent
    facts = filing.get_all_facts()
    assert calculation_network_good.is_aggregation_consistent(
        facts
    ), "Good calculation network is not aggregation consistent"

    # check that the bad network is not balance consistent
    assert not calculation_network_bad.is_balance_consistent(), "Bad calculation network is balance consistent"

    # check that the bad network is not aggregation consistent
    assert not calculation_network_bad.is_aggregation_consistent(
        facts
    ), "Bad calculation network is aggregation consistent"
