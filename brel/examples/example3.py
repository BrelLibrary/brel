from brel import Filing, Aspect
from brel.utils import pprint


def example3():
    """
    Example of how to get some reported concets, get all facts that use those concepts, and print them.
    """

    filing = Filing.open("reports/aapl/")

    # get some concepts
    concepts = filing.get_all_reported_concepts()[:6]

    # get all facts that use those concepts
    facts = []
    for concept in concepts:
        facts += filing.get_facts_by_concept(concept)

    # pretty print them
    pprint(facts)
