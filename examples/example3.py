from brel import Filing, Aspect
from brel.utils import pprint


def example3():
    """
    Example of how to get some reported concets, get all facts that use those concepts, and print them.
    """

    # MAKE SURE TO CHANGE THIS TO THE PATH OF THE FILING YOU WANT TO USE
    print(
        "MAKE SURE TO CHANGE THE PATH IN EXAMPLE1.PY TO THE PATH OF THE FILING YOU WANT TO USE"
    )
    filing = Filing.open("reports/report.zip")

    concept = filing.get_concept_by_name("us-gaap:Assets")
    facts = filing.get_all_facts()
    facts = list(
        filter(
            lambda fact: str(fact.get_characteristic(Aspect.UNIT)) == "usd"
            and str(fact.get_characteristic(Aspect.CONCEPT)) == "us-gaap:Assets",
            facts,
        )
    )

    pprint(facts)


if __name__ == "__main__":
    example3()
