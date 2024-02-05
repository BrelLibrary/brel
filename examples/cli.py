import argparse, brel

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="?")
parser.add_argument("--facts", default=None)
parser.add_argument("--components", default=None)
args = parser.parse_args()

# Load the report
report = brel.Filing.open(args.file)

if args.facts:
    # Get the facts, filter them and print them.
    facts = [
        fact
        for fact in report.get_all_facts()  # gets all facts from the report
        if args.facts == str(fact.get_concept())  # filter by concept or
        or args.facts in map(str, fact.get_aspects())  # filter by any aspect
    ]
    brel.utils.pprint(facts)
elif args.components:
    # Get the components that match the filter and print them.
    components = [
        component
        for component in report.get_all_components()  # get all components
        if args.components in component.get_URI()  # filter by URI
    ]
    brel.utils.pprint(components)
