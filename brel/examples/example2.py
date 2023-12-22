from brel import Filing
from random import randint, sample
from brel.utils import pprint_fact, pprint_facts

def example2():
    """
    Example of how to get all of the facts from a filing and print one of them.
    """

    # load the filing
    filing = Filing.open("reports/tsla")

    # get all of the facts
    facts = filing.get_all_facts()

    # get some random facts
    random_fact = facts[randint(0, len(facts) - 1)]

    # pretty print a single fact
    pprint_fact(random_fact)

    # pretty print 10 random facts
    pprint_facts(sample(facts, 10))

    # count the number of components in the filing
    print("Number of components: {}".format(len(filing.get_all_components())))