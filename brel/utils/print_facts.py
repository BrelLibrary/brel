"""
Module for pretty printing facts as a table to the console.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 29 December 2023

====================
"""

from prettytable import PrettyTable

from brel import Fact
from brel.characteristics import Aspect


def pprint_facts(facts: list[Fact]):
    """
    Print a list of facts in a pretty table.
    """

    # first extract all the dimensions from the facts
    dimension_set = set()
    for fact in facts:
        context = fact.get_context()
        for aspect in context.get_aspects():
            dimension_set.add(aspect)

    dimensions = list(dimension_set)

    # helper function for sorting dimensions
    # sorts in the following order
    # 1. concept
    # 2. period
    # 3. entity
    # 4. unit
    # 5. additional dimensions in alphabetical order
    def sort_dimensions(dimension: Aspect) -> str:
        if dimension == Aspect.CONCEPT:
            return "1"
        elif dimension == Aspect.PERIOD:
            return "2"
        elif dimension == Aspect.ENTITY:
            return "3"
        elif dimension == Aspect.UNIT:
            return "4"
        else:
            return "5" + dimension.get_name()

    dimensions.sort(key=sort_dimensions)

    # initialize the table
    columns = ["id"] + [dimension.get_name() for dimension in dimensions] + ["value"]

    table = PrettyTable(columns)
    table.align = "r"
    table.title = "Facts Table"

    # extract the rows from the facts
    rows = []
    for fact in facts:
        context = fact.get_context()
        row = (
            [fact._get_id()]  # pylint: disable=protected-access
            + [context.get_characteristic(dimension) for dimension in dimensions]
            + [fact.get_value_as_str()]
        )

        rows.append(row)

    # rows.sort(key=lambda row: int(row[0].split("-")[1]))
    # sort rows alphabetically by the fact id
    # rows.sort(key=lambda row: row[0])
    rows.sort(key=lambda row: row[0] if isinstance(row[0], str) else "")

    # add the rows to the table and print it
    for row in rows:
        table.add_row(row)

    print(table)


def pprint_fact(fact: Fact):
    """
    Prints a single fact in a pretty table.
    """

    # initialize the table
    columns = ["aspect", "value"]

    # alignment = ["r"] * (len(columns) - 1) + ["l"]
    alignment = "l"
    # print(alignment)

    table = PrettyTable(columns, align=alignment)
    # table.align = "r"
    # table.align["value"] = "l"
    table.title = "Fact Table"

    # extract the rows from the fact
    rows = []
    context = fact.get_context()
    for aspect in context.get_aspects():
        rows.append([aspect.get_name(), context.get_characteristic(aspect)])

    rows.sort(key=lambda row: row[0] if isinstance(row[0], str) else "")

    # add the rows to the table and print it
    for row in rows:
        table.add_row(row)

    table.add_row(["value", fact.get_value_as_str()])

    print(table)
