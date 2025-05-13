"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""

from typing import List, Type

from brel.brel_component import Component
from brel.brel_fact import Fact
from brel.brel_filing import Filing
from brel.networks.i_network import INetwork
from brel.reportelements.abstract import Abstract
from brel.reportelements.concept import Concept
from brel.reportelements.dimension import Dimension
from brel.reportelements.hypercube import Hypercube
from brel.reportelements.i_report_element import IReportElement
from brel.reportelements.lineitems import LineItems
from brel.reportelements.member import Member


def assert_list_of_type[T](lst: List[T], type_: Type[T]):
    assert isinstance(lst, list), f"Expected list, got {type(lst)}"
    assert all(isinstance(x, type_) for x in lst), f"Expected all {type_}, got {lst}"


def test_filing_getters():
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")

    # check get_all_facts(). it should return a list of facts
    facts = filing.get_all_facts()
    assert_list_of_type(facts, Fact)

    # check if get_all_report_elements(). it should return a list of report elements
    report_elements = filing.get_all_report_elements()
    assert_list_of_type(report_elements, IReportElement)

    # check get_all_components(). it should return a list of components
    components = filing.get_all_components()
    assert_list_of_type(components, Component)

    # check get_all_physical_networks(). it should return a list of networks
    networks = filing.get_all_physical_networks()
    assert_list_of_type(networks, INetwork)

    # check get_errors(). it should return a list of errors
    errors = filing.get_errors()
    assert_list_of_type(errors, Exception)

    # check get_all_abstracts(). it should return a list of abstracts
    abstracts = filing.get_all_abstracts()
    assert_list_of_type(abstracts, Abstract)

    # check get_all_dimensions(). it should return a list of dimensions
    dimensions = filing.get_all_dimensions()
    assert_list_of_type(dimensions, Dimension)

    # check get_all_hypercubes(). it should return a list of hypercubes
    hypercubes = filing.get_all_hypercubes()
    assert_list_of_type(hypercubes, Hypercube)

    # check get_all_members(). it should return a list of members
    members = filing.get_all_members()
    assert_list_of_type(members, Member)

    # check get_all_concepts(). it should return a list of concepts
    concepts = filing.get_all_concepts()
    assert_list_of_type(concepts, Concept)

    # check get_all_line_items(). it should return a list of line items
    line_items = filing.get_all_line_items()
    assert_list_of_type(line_items, LineItems)

    # check get_report_element_by_name(). it should return a report element
    report_element = filing.get_report_element_by_name("ete:cash")
    assert isinstance(
        report_element, Concept
    ), f"Expected Concept, got {type(report_element)}"

    # check get_concept_by_name(). it should return a concept
    concept = filing.get_concept_by_name("ete:cash")
    assert isinstance(concept, Concept), f"Expected Concept, got {type(concept)}"

    # check the get_concept() method. it should return the concept from before
    assert concept == filing.get_concept(
        concept.get_name()
    ), "Expected the same concept"

    # check if get_all_reported_concepts contains the cash concept
    assert (
        concept in filing.get_all_reported_concepts()
    ), "Expected the concept to be in the reported concepts"

    # check get_facts_by_concept_name(). all facts should have the cash concept
    facts = filing.get_facts_by_concept_name("ete:cash")
    assert_list_of_type(facts, Fact)
    assert all(
        f.get_concept().get_value() == concept for f in facts
    ), "Expected all facts to have the cash concept"

    # check get_facts_by_concept(). all facts should have the cash concept
    facts = filing.get_facts_by_concept(concept)
    assert_list_of_type(facts, Fact)
    assert all(
        f.get_concept().get_value() == concept for f in facts
    ), "Expected all facts to have the cash concept"

    # check if get_all_component_uris() contains the uris "http://foo/role/balance", "http://foo/role/hypercube" and "http://foo/role/bad-balance"
    uris = filing.get_all_component_uris()
    assert (
        "http://foo/role/balance" in uris
    ), "Expected the uri 'http://foo/role/balance' to be in the list"
    assert (
        "http://foo/role/hypercube" in uris
    ), "Expected the uri 'http://foo/role/hypercube' to be in the list"
    assert (
        "http://foo/role/bad-balance" in uris
    ), "Expected the uri 'http://foo/role/bad-balance' to be in the list"

    component = filing.get_component("http://foo/role/balance")
    assert component == filing.get_component(
        component.get_URI()
    ), "Expected the same component"


def test_filing_open():
    try:
        filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
        assert (
            len(filing.get_errors()) == 0
        ), f"Expected no errors, got {filing.get_errors()}"
    except Exception as e:
        assert False, f"Expected no exception, got {e}"

    try:
        filing = Filing.open(".")
        assert False, "Expected an exception when opening a folder with no xml files"
    except Exception as e:
        pass

    try:
        filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
        assert (
            len(filing.get_errors()) == 0
        ), f"Expected no errors, got {filing.get_errors()}"
    except Exception as e:
        assert False, f"Expected no exception, got {e}"

    try:
        filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
        assert (
            len(filing.get_errors()) == 0
        ), f"Expected no errors, got {filing.get_errors()}"
    except Exception as e:
        assert False, f"Expected no exception, got {e}"

    try:
        filing = Filing.open("invalid_path")
        assert False, "Expected an exception when opening an invalid path"
    except Exception as e:
        pass


if __name__ == "__main__":
    test_filing_getters()
    test_filing_open()
