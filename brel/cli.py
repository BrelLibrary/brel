"""
CLI interface for brel project.
"""

import os
import argparse
from brel import *


# import argparser
import sys


def main():  # pragma: no cover
    print("Brel is a Python library for working with XBRL filings.")
    print(
        "For documentation on how to use brel, see https://papedipoo.github.io/Brel/"
    )

    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog="brel",
        description="Brel is a Python library for working with XBRL filings.",
    )

    # create subparsers
    subparsers = parser.add_subparsers(help="sub-command help")

    # create the parser for the "load" command
    parser_load = subparsers.add_parser("load", help="load help")
    parser_load.add_argument(
        "path", type=str, help="Path to the XBRL filing to load."
    )

    # if the user wants to load a filing, do so
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        args = parser.parse_args()
        if os.path.exists(args.path):
            filing = Filing.open(args.path)
            print("Loaded filing")
            facts = filing.get_all_facts()
            print(f"Found {len(facts)} facts.")
            reportelements = filing.get_all_report_elements()
            print(f"Found {len(reportelements)} report elements.")
            contexts = filing.get_all_components()
            print(f"Found {len(contexts)} contexts.")

        else:
            print(f"Path {args.path} does not exist.")
        return
