from brel import Filing
from random import sample

def example1():
    """
    Example of how to use brel to open a filing and get all reported the report elements and print some of their labels 
    """

    # open the filing
    # resolves the DTS and caches it
    # currently only supports local paths pointing towards a directory
    filing = Filing.open("reports/coca_cola/")

    # get all reported report elements and take a sample of 10 
    all_elements = filing.get_all_reported_concepts()
    some_elements = sample(all_elements, 10)

    # print the names of the concepts
    for concept in some_elements:
        print("-"*20)
        print(concept)

        # print the labels of the concepts
        labels = concept.get_labels()

        for label in labels:
            print(f"{label.get_language()} : {label.get_label_role().value:20} : {label}")
    
