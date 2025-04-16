from brel import Filing
from brel.resource import BrelLabel
from brel.reportelements import *
from brel.networks import *


def test_end_to_end_labels():
    """
    Tests the labels of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    report_elements = filing.get_all_report_elements()

    for report_element in report_elements:
        re_prefix = report_element.get_name().get_prefix().lower()

        if re_prefix != "ete":
            continue

        assert (
            len(report_element.get_labels()) <= 1
        ), f"Report element {report_element.get_name()} has more than one label {report_element.get_labels()}"

        for label in report_element.get_labels():
            assert (
                label.get_label_role() == BrelLabel.STANDARD_LABEL_ROLE
            ), f"Label {label.get_content()} of report element {report_element.get_name()} has a non-standard role {label.get_label_role()}"


def test_end_to_end_components():
    """
    Tests the components of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")

    # check the calculation networks
    components = filing.get_all_components()
    calculation_networks = [
        component.get_calculation_network()
        for component in components
        if component.get_calculation_network() is not None
    ]

    assert (
        len(calculation_networks) == 2
    ), f"Expected two calculation networks, got {len(calculation_networks)}"

    assert any(
        component.get_URI() == "http://foo/role/balance" for component in components
    ), "No component with URI 'http://foo/role/balance' found"

    assert any(
        component.get_URI() == "http://foo/role/hypercube" for component in components
    ), "No component with URI 'http://foo/role/hypercube' found"

    assert (
        "http://foo/role/balance" in filing.get_all_component_uris()
    ), "URI 'http://foo/role/balance' not in get_all_component_uris()"

    assert (
        "http://foo/role/hypercube" in filing.get_all_component_uris()
    ), "URI 'http://foo/role/hypercube' not in get_all_component_uris()"

    balance_component = filing.get_component("http://foo/role/balance")
    assert (
        balance_component.get_calculation_network() is not None
    ), "Balance component has no calculation network"

    assert (
        balance_component.get_presentation_network() is not None
    ), "Balance component has no presentation network"

    assert (
        balance_component.get_definition_network() is None
    ), "Balance component has a definition network"


if __name__ == "__main__":
    test_end_to_end_labels()
    test_end_to_end_components()
