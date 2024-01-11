from brel import Filing, pprint
from brel.reportelements import *
from brel.networks import *
from typing import cast


def test_end_to_end():
    filing = Filing.open("tests/end_to_end/ete_filing")

    report_elements = filing.get_all_report_elements()

    # print the components
    for component in filing.get_all_components():
        print(component.get_URI())
        presentation = component.get_presentation_network()
        if presentation is not None:
            pprint(presentation)
        calculation = component.get_calculation_network()
        if calculation is not None:
            pprint(calculation)
        definition = component.get_definition_network()
        if definition is not None:
            pprint(definition)

    # print all physical networks
    for physical_network in filing.get_all_physical_networks():
        pprint(physical_network)

    # check the report elements
    # check that all report elements have different names
    for report_element in report_elements:
        re_name = report_element.get_name()
        assert (
            len([re for re in report_elements if re.get_name() == re_name])
            == 1
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

        # check if all report elements do not have more than one label
        assert (
            len(report_element.get_labels()) <= 1
        ), f"Report element {report_element.get_name()} has more than one label"

        # check that all label roles are standard labels
        for label in report_element.get_labels():
            assert (
                label.get_label_role().value == "label"
            ), f"Label {label.get_content()} of report element {report_element.get_name()} has a non-standard role {label.get_label_role().value}"

    # check the calculation networks
    components = filing.get_all_components()
    calculation_networks = [
        component.get_calculation_network()
        for component in components
        if component.get_calculation_network() is not None
    ]

    assert (
        len(calculation_networks) == 1
    ), f"Expected one calculation network, got {len(calculation_networks)}"

    calculation_network = cast(CalculationNetwork, calculation_networks[0])

    # check that it is balance consistent
    assert (
        calculation_network.is_balance_consisent()
    ), "Calculation network is not balance consistent"

    # check that the network is aggregation consistent
    facts = filing.get_all_facts()

    pprint(facts)
    pprint(calculation_network)
    assert calculation_network.is_aggregation_consistent(
        facts
    ), "Calculation network is not aggregation consistent"


if __name__ == "__main__":
    test_end_to_end()
