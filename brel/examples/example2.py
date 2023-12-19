from brel import Filing
from random import randint
from brel.utils import pprint_fact

def example2():
    """
    Example of how to get all of the facts from a filing and print one of them.
    """

    # load the filing
    filing = Filing.open("reports/ko/")

    # get all of the facts
    facts = filing.get_all_facts()

    # get one random fact
    fact = facts[randint(0, len(facts) - 1)]

    # pretty print it
    pprint_fact(fact)