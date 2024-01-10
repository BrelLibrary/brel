from brel import Filing
from brel.utils import pprint


def example1():
    """
    Example of how to use brel to open a filing and get all reported the report elements and print some of their labels
    """

    # open the filing
    # resolves the DTS and caches it
    # currently only supports local paths pointing towards a directory
    filing = Filing.open("reports/aapl.zip")

    # get the us-gaap:Assets concept
    assets_concept = filing.get_concept_by_name("us-gaap:Assets")

    if assets_concept is None:
        raise ValueError("Could not find the concept us-gaap:Assets")

    # get all facts that report against the assets concept
    assets_facts = filing.get_facts_by_concept(assets_concept)

    # print the facts
    pprint(assets_facts)
