"""
This module tests the calculation validation functions.
# TODO: Add more validation tests
# TODO: Add parsing tests

@author: Robin Schmidiger
@version: 0.1
@date: 29 December 2023
"""

from brel import QName, QNameNSMap, Fact, Context, ConceptCharacteristic
from brel.networks import CalculationNetwork, CalculationNetworkNode
from brel.reportelements import Concept
from brel.utils import pprint_network, pprint_facts

DEBUG = False

nsmap = QNameNSMap()
nsmap.add_to_nsmap("https://xbrl.fasb.org/us-gaap/2023", "us-gaap")
nsmap.add_to_nsmap("http://www.xbrl.org/2003/linkbase", "link")

qnames = [
    QName.from_string("us-gaap:Assets", nsmap),
    QName.from_string("us-gaap:CurrentAssets", nsmap),
    QName.from_string("us-gaap:CashAndCashEquivalentsAtCarryingValue", nsmap),
    QName.from_string("us-gaap:InventoryNet", nsmap),
    QName.from_string("us-gaap:RawMaterialsAndSupplies", nsmap),
    QName.from_string("us-gaap:ValuationReserves", nsmap),
    QName.from_string("us-gaap:LIFOReserve", nsmap),
    QName.from_string("us-gaap:NoncurrentAssets", nsmap),
    QName.from_string("us-gaap:InventoryNoncurrent", nsmap),
    QName.from_string("us-gaap:PropertyPlantAndEquipmentNet", nsmap),
]

concepts = [
    Concept(qnames[0], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[1], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[2], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[3], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[4], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[5], [], "duration", "credit", False, "monetaryItemType"),
    Concept(qnames[6], [], "duration", "credit", False, "monetaryItemType"),
    Concept(qnames[7], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[8], [], "duration", "debit", False, "monetaryItemType"),
    Concept(qnames[9], [], "duration", "debit", False, "monetaryItemType"),
]

arc_role = "http://www.xbrl.org/2003/arcrole/summation-item"
arc_name = QName.from_string("link:calculationLink", nsmap)
link_role = "CONDENSEDCONSOLIDATEDSTATEMENTSOFINCOME"
link_name = QName.from_string(
    "us-gaap:CondensedConsolidatedStatementsOfIncome", nsmap
)


def create_node(concept: Concept, weight: int, order: int):
    return CalculationNetworkNode(
        concept, [], arc_role, arc_name, link_role, link_name, weight, order
    )


def fact_from_concept(concept: Concept, value: str):
    context = Context("unspecified")
    concept_characteristic = ConceptCharacteristic(concept)
    context._add_characteristic(concept_characteristic)
    return Fact(context, value, "unspecified")


def test_calculation_validation_GD():
    # The following code creates the following calculation network:
    #
    # Assets
    #   Current Assets
    #     Cash and Cash Equivalents at Carrying Value
    #     Inventory, Net
    #       Raw Materials and Supplies
    #       Valuation Reserves (weight = -1)
    #       LIFO Reserve (weight = -1)
    #   Noncurrent Assets
    #     Inventory, Noncurrent
    #     Property, Plant and Equipment, Net
    #
    # With the following facts:
    # Assets: 100
    # Current Assets: 80
    # Cash and Cash Equivalents at Carrying Value: 10
    # Inventory, Net: 70
    # Raw Materials and Supplies: 200
    # Valuation Reserves: 55
    # LIFO Reserve: 75
    # Noncurrent Assets: 20
    # Inventory, Noncurrent: 15
    # Property, Plant and Equipment, Net: 5
    #
    # The network is balance consistent and aggregation consistent

    nodes = [
        create_node(concepts[0], 1, 1),
        create_node(concepts[1], 1, 1),
        create_node(concepts[2], 1, 1),
        create_node(concepts[3], 1, 2),
        create_node(concepts[4], 1, 1),
        create_node(concepts[5], -1, 2),
        create_node(concepts[6], -1, 3),
        create_node(concepts[7], 1, 2),
        create_node(concepts[8], 1, 1),
        create_node(concepts[9], 1, 2),
    ]

    nodes[0]._add_child(nodes[1])
    nodes[1]._add_child(nodes[2])
    nodes[1]._add_child(nodes[3])
    nodes[3]._add_child(nodes[4])
    nodes[3]._add_child(nodes[5])
    nodes[3]._add_child(nodes[6])
    nodes[0]._add_child(nodes[7])
    nodes[7]._add_child(nodes[8])
    nodes[7]._add_child(nodes[9])

    facts = [
        fact_from_concept(concepts[0], "100"),
        fact_from_concept(concepts[1], "80"),
        fact_from_concept(concepts[2], "10"),
        fact_from_concept(concepts[3], "70"),
        fact_from_concept(concepts[4], "200"),
        fact_from_concept(concepts[5], "55"),
        fact_from_concept(concepts[6], "75"),
        fact_from_concept(concepts[7], "20"),
        fact_from_concept(concepts[8], "15"),
        fact_from_concept(concepts[9], "5"),
    ]

    network = CalculationNetwork([nodes[0]], link_role, link_name)

    if DEBUG:  # pragma: no cover
        pprint_network(network)

        print(network.is_balance_consisent())
        print(network.is_aggregation_consistent(facts))

    assert network.is_balance_consisent()
    assert network.is_aggregation_consistent(facts)


def test_calculation_validation_NG_balance():
    # The following code creates the following calculation network:
    #
    # Inventory, Net
    #   Raw Materials and Supplies
    #   Valuation Reserves (weight = 1, but should be -1 because the balance is credit)

    # the network is not balance consistent because

    nodes = [
        create_node(concepts[3], 1, 1),
        create_node(concepts[4], 1, 1),
        create_node(concepts[5], 1, 1),
    ]

    nodes[0]._add_child(nodes[1])
    nodes[0]._add_child(nodes[2])

    network = CalculationNetwork([nodes[0]], link_role, link_name)

    if DEBUG:  # pragma: no cover
        pprint_network(network)

    assert (
        not network.is_balance_consisent()
    ), "The edge Inventory, Net -> Valuation Reserves should have weight -1 since the former is debit and the latter is credit"

    # The following code creates the following calculation network:
    #
    # Assets
    #   Current Assets (weight = -1 but should be 1 because the balance is debit)
    #     Cash and Cash Equivalents at Carrying Value

    # the network is not balance consistent

    nodes = [
        create_node(concepts[0], 1, 1),
        create_node(concepts[1], -1, 1),
        create_node(concepts[2], 1, 1),
    ]

    nodes[0]._add_child(nodes[1])
    nodes[1]._add_child(nodes[2])

    network = CalculationNetwork([nodes[0]], link_role, link_name)

    if DEBUG:  # pragma: no cover
        pprint_network(network)

    assert (
        not network.is_balance_consisent()
    ), "The edge Assets -> Current Assets should have weight 1 since both are debit"


def test_calculation_validation_GD_empty_network():
    # check if the empty network is aggregation consistent
    network = CalculationNetwork([], link_role, link_name)

    if DEBUG:  # pragma: no cover
        pprint_network(network)

    assert network.is_aggregation_consistent(
        []
    ), "The empty network should be aggregation consistent"

    facts = []

    assert network.is_aggregation_consistent(
        facts
    ), "The empty network should be aggregation consistent"


def test_calculation_validation_NG_aggregation():
    # The following code creates the following calculation network:
    #
    # Assets (weight = 1)
    #   Current Assets (weight = 1)
    #     Cash and Cash Equivalents at Carrying Value (weight = 1)
    #     Inventory, Net (weight = 1)

    # Assets: 100
    # Current Assets: 80
    # Cash and Cash Equivalents at Carrying Value: 10
    # Inventory, Net: 70

    # the network is not aggregation consistent because the children of Assets (Current Assets) do not add up to 100

    nodes = [
        create_node(concepts[0], 1, 1),
        create_node(concepts[1], 1, 1),
        create_node(concepts[2], 1, 1),
        create_node(concepts[3], 1, 1),
    ]

    nodes[0]._add_child(nodes[1])
    nodes[1]._add_child(nodes[2])
    nodes[1]._add_child(nodes[3])

    facts = [
        fact_from_concept(concepts[0], "100"),
        fact_from_concept(concepts[1], "80"),
        fact_from_concept(concepts[2], "10"),
        fact_from_concept(concepts[3], "70"),
    ]

    network = CalculationNetwork([nodes[0]], link_role, link_name)

    if DEBUG:  # pragma: no cover
        pprint_network(network)
        pprint_facts(facts)

    print(network.is_aggregation_consistent(facts))

    assert not network.is_aggregation_consistent(
        facts
    ), "The children of Assets do not add up to 100. The network should not be aggregation consistent"


if __name__ == "__main__":
    test_calculation_validation_GD()
    # test_calculation_validation_NG_aggregation()
    # test_calculation_full()
