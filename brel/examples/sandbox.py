from brel import *
from brel.utils import *
from random import randint


def sandbox():
    # open the filing
    filing = Filing.open("reports/ko/")

    # # example for filtering for a specific concept
    # filtered_facts = filing[filing["concept"] == "us-gaap:Revenues"]

    # pprint_facts(filtered_facts)

    # # example for filtering for a specific concept and an additional dimension
    # # for the additional dimension, we want either latin america or north america
    # filtered_facts = filing[
    #     (filing["concept"] == "us-gaap:Revenues")
    #     & (
    #         (filing["us-gaap:StatementBusinessSegmentsAxis"] == "ko:LatinAmericaSegmentMember")
    #         | (filing["us-gaap:StatementBusinessSegmentsAxis"] == "ko:NorthAmericaSegmentMember"))
    # ]

    # pprint_facts(filtered_facts)
