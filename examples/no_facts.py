import brel
import argparse

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="?")

args = parser.parse_args()
report = brel.Filing.open(args.file)
facts = report.get_all_facts()
print(len(facts))
