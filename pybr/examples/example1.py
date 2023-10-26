from pybr import PyBRFiling

def example1():
    """
    Example of how to use pybr to open a filing and get all the concepts. 
    """

    # open the filing
    # resolves the DTS and caches it
    # currently only supports local paths pointing towards a directory
    filing = PyBRFiling.open("reports/coca_cola/")

    # get the first 100 concepts
    some_concepts = filing.get_all_concepts()[:20]

    # print them
    for concept in some_concepts:
        print(concept)