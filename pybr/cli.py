"""CLI interface for pybr project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

import os
from prettytable import PrettyTable
from pybr import *

def print_facts_as_table(facts : list[PyBRFact]):
    # find all the additional columns by looking at all the contexts and finding all the dimensions axis
    additional_dimensions: dict[str, PyBRDimension] = {}

    # additional_columns = list(additional_columns)
    for fact in facts:
        context: PyBRContext = fact.get_context()
        # print(context.get_aspects())
        for aspect in context.get_aspects():
            if aspect.is_core():
                continue
            additional_dimensions[aspect.get_name()] = aspect
    
    additional_columns = list(additional_dimensions.keys())
    additional_columns.sort()

    # columns = ["id", "concept", "entity", "period", "unit"] + list(additional_columns) + ["value"]
    columns = ["id", "concept", "entity", "period", "unit"] + additional_columns + ["value"]
    table = PrettyTable(columns)
    table.align = "r"
    table.align["value"] = "l"
    table.title = "Facts Table"

    rows = []

    for fact in facts:
        context: PyBRContext = fact.get_context()
        row = [fact.get_id(),
               context.get_value_as_object(PyBRAspect.CONCEPT),
               context.get_value_as_object(PyBRAspect.ENTITY),
                context.get_value_as_object(PyBRAspect.PERIOD),
                context.get_value_as_object(PyBRAspect.UNIT)]
        for additional_column in additional_columns:
            row.append(context.get_value_as_object(additional_dimensions[additional_column]))
        row.append(fact.get_value())
        
        # table.add_row(row)
        rows.append(row)
    
    rows.sort(key=lambda row: row[0])

    for row in rows:
        table.add_row(row)

    print(table)

def main():  # pragma: no cover
    print("running main")
    print(f"working dir: {os.getcwd()}")

    # clear the cache
    # for file in os.listdir("pybr/dts_cache/"):
    #     os.remove("pybr/dts_cache/" + file)

    # In general, all the classes that I have created start with the prefix "PyBR"
    # so things like "PyBRFact", "PyBREntity" or "PyBRContext"
    filing = PyBRFiling.open("reports/coca_cola/")

    concept_names: list[QName] = [x.get_name() for x in filing.get_all_concepts()]

    # print(concept_names)
    for concept_name in concept_names[:100]:
        print(concept_name, end=", ")
    print()

    concept_names = [
        QName("http://xbrl.sec.gov/dei/2023", "dei", "SecurityExchangeName"),
        QName("http://fasb.org/us-gaap/2023", "us-gaap", "OtherComprehensiveIncomeLossTaxPortionAttributableToParent1")
    ]

    # get all the facts that are associated with the three concepts
    facts = []
    for concept_name in concept_names:
        facts += filing.get_facts_by_concept_name(concept_name)

    # This prints all facts that are associated with the three concepts
    print_facts_as_table(facts)



