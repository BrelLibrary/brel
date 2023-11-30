"""
CLI interface for pybr project.
"""

import os
from pybr import *
from pybr.examples import *

# import argparser
import sys

def main():  # pragma: no cover
    print("running main")
    print(f"working dir: {os.getcwd()}")

    # parse the arguments

    if "c" in sys.argv:
        # clear the cache
        for file in os.listdir("pybr/dts_cache/"):
            os.remove("pybr/dts_cache/" + file)

    if "1" in sys.argv:
        # execute example 1
        print("[RUNNING EXAMPLE 1]")
        example1()
        print()
    
    if "2" in sys.argv:
        # execute example 2
        print("[RUNNING EXAMPLE 2]")
        example2()
        print()
    
    if "3" in sys.argv:
        # execute example 3
        print("[RUNNING EXAMPLE 3]")
        example3()
        print()
    
    if "4" in sys.argv:
        # execute example 4
        print("[RUNNING EXAMPLE 4]")
        example4()
        print()

    if "5" in sys.argv:
        # execute example 5
        print("[RUNNING EXAMPLE 5]")
        example5()
        print()
    
    if "6" in sys.argv:
        # execute example 6
        print("[RUNNING EXAMPLE 6]")
        example6()
        print()
    
    if "7" in sys.argv:
        # execute example 7
        print("[RUNNING EXAMPLE 7]")
        example7()
        print()
    
    if "s" in sys.argv:
        # execute sandbox
        print("[RUNNING SANDBOX]")
        sandbox()
        print()
