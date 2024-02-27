import brel
from brel.utils import pprint_fact, pprint_facts
import os, sys
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


def test_print_fact():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    fact = filing.get_facts_by_concept_name("ete:cash")[0]
    output = method_output_to_string(lambda: pprint_fact(fact))

    # check if the printed fact is as expected
    # check if ete:cash is printed
    assert "ete:cash" in output, f"ete:cash not in {output}"
    # check if 1234 is printed (entity)
    assert "1234" in output, f"1234 not in {output}"
    # check if usd is printed (unit)
    assert "USD" in output, f"usd not in {output}"


def test_print_facts():
    filing = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    facts = filing.get_facts_by_concept_name("ete:cash")
    output = method_output_to_string(lambda: pprint_facts(facts))

    # check if the printed facts are as expected
    # check if ete:cash is printed
    assert "ete:cash" in output, f"ete:cash not in {output}"
    # check if 1234 is printed (entity)
    assert "1234" in output, f"1234 not in {output}"
    # check if the fact id 'f-003' is printed
    assert "f-003" in output, f"f-003 not in {output}"
    # check if the unit USD is printed
    assert "USD" in output, f"USD not in {output}"
