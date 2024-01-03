from brel import *
from brel.utils import *
from random import randint
from typing import cast


def sandbox():
    # open the filing
    filing = Filing.open("reports/ko/")

    # get all report elements
    report_elements = filing.get_all_report_elements()

    # get the longest qname of the report elements
    def len_of_qname(element: IReportElement):
        qname = element.get_name()
        return len(qname.get())

    longest_qname = max(report_elements, key=len_of_qname)

    print("Longest qname: ", longest_qname.get_name())

    # get the concept us-gaap:Revenue
    revenue = next(
        filter(lambda x: x.get_name().get() == "us-gaap:Revenues", report_elements)
    )
    revenue = cast(Concept, revenue)

    print(revenue.__dict__)

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
