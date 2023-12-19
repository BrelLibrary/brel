from brel import Filing
from brel.utils import pprint_facts

def example1():
    """
    Example of how to use brel to open a filing and get all reported the report elements and print some of their labels 
    """

    # open the filing
    # resolves the DTS and caches it
    # currently only supports local paths pointing towards a directory
    filing = Filing.open("reports/aapl.zip")

    # get the us-gaap:Assets concept
    assets_concept = filing.get_report_element_by_name("us-gaap:Assets")

    # get all facts that report against the assets concept
    assets_facts = filing.get_facts_by_concept(assets_concept)

    # print the facts
    pprint_facts(assets_facts)

    # alternative version using pandas notation
    assets_facts = filing[filing["concept"] == "us-gaap:Assets"]

    pprint_facts(assets_facts)
