from brel import Filing
from random import randint, sample
from brel.utils import pprint


def example2():
    """
    Example of how to get all of the facts from a filing and print one of them.
    """

    # MAKE SURE TO CHANGE THIS TO THE PATH OF THE FILING YOU WANT TO USE
    print(
        "MAKE SURE TO CHANGE THE PATH IN EXAMPLE1.PY TO THE PATH OF THE FILING YOU WANT TO USE"
    )
    filing = Filing.open("reports/report.zip")

    # get all of the facts
    facts = filing.get_all_facts()

    # get some random facts
    random_fact = facts[randint(0, len(facts) - 1)]

    # pretty print a single fact
    pprint(random_fact)

    # pretty print 10 random facts
    pprint(sample(facts, 10))

    # count the number of components in the filing
    print("Number of components: {}".format(len(filing.get_all_components())))


if __name__ == "__main__":
    example2()
