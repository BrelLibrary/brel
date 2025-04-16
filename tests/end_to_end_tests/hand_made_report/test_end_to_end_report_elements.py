from brel import Filing
from brel.resource import BrelLabel
from brel.reportelements import *
from brel.networks import *


def test_end_to_end_report_element_types():
    """
    Tests the report elements of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")

    report_elements = [
        re
        for re in filing.get_all_report_elements()
        if re.get_name().get_prefix() == "ete"
    ]

    for report_element in report_elements:
        re_name = report_element.get_name()
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


def test_end_to_end_report_element_counts():
    """
    Tests the counts of the report elements of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    # check that there are exactly 15 concepts
    concepts = [
        concept
        for concept in filing.get_all_concepts()
        if concept.get_name().get_prefix() == "ete"
    ]
    assert len(concepts) == 15, f"Expected 15 concepts, got {len(concepts)}"

    # check that there are exactly 4 abstracts
    abstracts = [
        abstract
        for abstract in filing.get_all_abstracts()
        if abstract.get_name().get_prefix() == "ete"
    ]
    assert len(abstracts) == 4, f"Expected 4 abstracts, got {len(abstracts)}"

    # check that there a single lineitems
    line_items = [
        line_item
        for line_item in filing.get_all_line_items()
        if line_item.get_name().get_prefix() == "ete"
    ]
    assert len(line_items) == 1, f"Expected 1 line item, got {len(line_items)}"

    # check that there is exactly one hypercube
    hypercubes = [
        hypercube
        for hypercube in filing.get_all_hypercubes()
        if hypercube.get_name().get_prefix() == "ete"
    ]
    assert len(hypercubes) == 1, f"Expected 1 hypercube, got {len(hypercubes)}"

    # check that there is exactly 1 dimension
    dimensions = [
        dimension
        for dimension in filing.get_all_dimensions()
        if dimension.get_name().get_prefix() == "ete"
    ]
    assert len(dimensions) == 1, f"Expected 1 dimension, got {len(dimensions)}"

    # check that there are exactly 2 members
    members = [
        member
        for member in filing.get_all_members()
        if member.get_name().get_prefix() == "ete"
    ]
    assert len(members) == 2, f"Expected 2 member, got {len(members)}"


def test_end_to_end_concept_cash():
    """
    Tests the cash concept of the end-to-end filing
    """
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    concept = filing.get_concept("ete:cash")

    assert concept.get_name().get_local_name() == "cash"
    assert concept.get_name().get_prefix() == "ete"
    assert concept.get_period_type() == "duration"
    assert concept.get_balance_type() == "debit"
    assert concept.get_data_type() == "xbrli:monetaryItemType"
    assert concept.is_nillable() is True
    assert concept.select_main_label().get_content() == "Cash"
    assert concept.select_main_label().get_label_role() == BrelLabel.STANDARD_LABEL_ROLE


if __name__ == "__main__":
    test_end_to_end_report_element_types()
    test_end_to_end_report_element_counts()
    test_end_to_end_concept_cash()
