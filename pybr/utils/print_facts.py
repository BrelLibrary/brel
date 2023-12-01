from pybr import PyBRFact, PyBRAspect, PyBRContext, PyBRFiling, BrelLabel, QName
from prettytable import PrettyTable

def pprint_facts(facts: list[PyBRFact]):
    """
    Print a list of facts in a pretty table.
    """

    # first extract all the dimensions from the facts
    dimensions = set()
    for fact in facts:
        context = fact.get_context()
        for aspect in context.get_aspects():
            dimensions.add(aspect)
    
    dimensions = list(dimensions)

    # helper function for sorting dimensions
    # sorts in the following order
    # 1. concept
    # 2. period
    # 3. entity
    # 4. unit
    # 5. additional dimensions in alphabetical order
    def sort_dimensions(dimension: PyBRAspect) -> str:
        if dimension == PyBRAspect.CONCEPT:
            return "1"
        elif dimension == PyBRAspect.PERIOD:
            return "2"
        elif dimension == PyBRAspect.ENTITY:
            return "3"
        elif dimension == PyBRAspect.UNIT:
            return "4"
        else:
            return "5" + dimension.get_name()
    
    dimensions.sort(key=sort_dimensions)

    # initialize the table
    columns = ["id"] + [dimension.get_name() for dimension in dimensions] + ["value"]

    table = PrettyTable(columns)
    table.align = "r"
    table.align["value"] = "l"
    table.title = "Facts Table"

    # extract the rows from the facts
    rows = []
    for fact in facts:
        context = fact.get_context()
        row = [fact._get_id()] + [context.get_characteristic(dimension) for dimension in dimensions] + [fact.get_value_as_str()]
        
        rows.append(row)
    
    rows.sort(key=lambda row: int(row[0].split("-")[1]))

    # add the rows to the table and print it
    for row in rows:
        table.add_row(row)
    
    print(table)

def pprint_fact(fact: PyBRFact):
    """
    Prints a single fact in a pretty table.
    """

    # initialize the table
    columns = ["aspect", "value"]

    table = PrettyTable(columns)
    table.align = "r"
    table.align["value"] = "l"
    table.title = "Fact Table"

    # extract the rows from the fact
    rows = []
    context = fact.get_context()
    for aspect in context.get_aspects():
        rows.append([aspect.get_name(), context.get_characteristic(aspect)])
    
    rows.sort(key=lambda row: row[0])

    # add the rows to the table and print it
    for row in rows:
        table.add_row(row)
    
    print(table)
