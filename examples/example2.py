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

    networks = filing.get_all_physical_networks()
    some_networks = sample(networks, 3)

    for network in some_networks:
        pprint(network)


if __name__ == "__main__":
    example2()
