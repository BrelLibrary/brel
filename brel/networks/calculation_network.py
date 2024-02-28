"""
This module contains the class for representing a calculation network.
A calculation network is a network of nodes that represent the calculation of a Component.
Calculation networks also contain helper functions for checking the consistency of the calculation network specifically.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 29 December 2023

====================
"""

DEBUG = False

from typing import Iterable, cast

from brel import Fact, QName
from brel.characteristics import Aspect, ICharacteristic
from brel.networks import CalculationNetworkNode, INetwork, INetworkNode
from brel.reportelements import *


class CalculationNetwork(INetwork):
    """
    The class for representing a calculation network.
    A calculation network is a network of nodes that indicate which concepts are calculated from which other concepts.
    """

    def __init__(
        self,
        roots: list[CalculationNetworkNode],
        link_role: str,
        link_name: QName,
        is_physical: bool,
    ) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, is_physical)

    # second class citizen
    def is_balance_consistent(self) -> bool:
        """
        Returns true if the network is balance consistent.
        A network is balance consistent iff, for each parent-child relationship
        - if the two concepts have the same balance (credit/credit or debit/debit), then the child weight must be positive
        - if the two concepts have different balances (credit/debit or debit/credit), then the child weight must be negative

        :returns bool: True iff the network is balance consistent
        """

        def is_subtree_balance_consistent(
            node: CalculationNetworkNode,
        ) -> bool:
            """
            Returns true if the subtree rooted at node is balance consistent.
            Operates recursively.
            Returns false if
            - Any parent or child balance is None
            - The parent and child balances are the same, but the child weight is negative
            - The parent and child balances are different, but the child weight is positive
            - Any child subtree is not balance consistent
            Returns true otherwise

            :param node: the root of the subtree to check
            :returns: True iff the subtree rooted at node is balance consistent
            """
            # get the balance of the parent
            parent_balance = node.get_concept().get_balance_type()
            if parent_balance is None:
                return False

            # check the balance of the children
            for child in node.get_children():
                child = cast(CalculationNetworkNode, child)

                child_balance = child.get_concept().get_balance_type()
                if child_balance is None:
                    return False

                if parent_balance == child_balance:
                    if child.get_weight() < 0:
                        return False
                else:
                    if child.get_weight() > 0:
                        return False

                # check the balance of the children of the child
                if not is_subtree_balance_consistent(child):
                    return False

            return True

        # check the balance of the roots
        for root in self.get_roots():
            root = cast(CalculationNetworkNode, root)
            if not is_subtree_balance_consistent(root):
                return False

        return True

    # def is_aggregation_consistent(self, facts: list[Fact]) -> bool:
    def is_aggregation_consistent(self, facts: list[Fact]) -> bool:
        """
        A calculation network is aggregation consistent iff for concepts of nodes, the sum of the fact values of the children equals the fact value of the parent.

        If there are multiple facts for a concept, but the facts have different dates, then aggregation consistency is checked for each date separately.
        This not only holds for the date aspect, but for all aspects of the fact.
        :param facts: the facts of the filing against which to check the aggregation consistency
        :returns bool: True iff the network is aggregation consistent
        """

        def is_subnetwork_aggregation_consistent(
            node: CalculationNetworkNode,
        ) -> bool:
            """
            Returns true if the subtree rooted at node is aggregation consistent.
            Operates recursively.
            Returns false if
            - the sum of all children values does not equal the parent value
            - any child subtree is not aggregation consistent
            Returns true otherwise
            """
            # if the node is a leaf, it is aggregation consistent
            # even though this case would be captured by the following code, it is more efficient to short circuit the trivial case without querying the facts
            if node.is_leaf():
                return True

            concept = node.get_concept()
            node_facts = list(
                filter(
                    lambda fact: fact.get_concept().get_value() == concept,
                    facts,
                )
            )

            for node_fact in node_facts:
                node_value = node_fact.get_value_as_float()

                if DEBUG:  # pragma: no cover
                    print(f"{node_fact._get_id()}: {node_value} = ", end=" ")

                # get the sum of the children values
                children_sum: float = 0
                for child in node.get_children():
                    child = cast(CalculationNetworkNode, child)
                    child_concept = child.get_concept()

                    # child facts are all facts with the same characteristics as the node fact, except for the concept
                    child_facts: Iterable[Fact] = facts
                    for node_aspect in node_fact.get_aspects():
                        # if the aspect is the concept, then get all fact with the child_concept as the concept characteristic
                        if node_aspect == Aspect.CONCEPT:
                            child_facts = list(
                                filter(
                                    lambda fact: fact.get_concept().get_value() == child_concept,
                                    child_facts,
                                )
                            )
                        else:
                            # otherwise, get all facts with the same characteristic as the node fact
                            node_characteristic = node_fact.get_characteristic(node_aspect)
                            child_facts = list(
                                filter(
                                    lambda fact: fact.get_characteristic(node_aspect) == node_characteristic,
                                    child_facts,
                                )
                            )

                    # there should only be one child fact left
                    all_child_facts = list(child_facts)
                    parent_characteristics = [
                        str(node_fact.get_characteristic(aspect))
                        for aspect in node_fact.get_aspects()
                        if aspect != Aspect.CONCEPT
                    ]
                    if len(all_child_facts) == 0:
                        raise ValueError(
                            f"Could not find a fact for concept {child_concept} with characteristics {parent_characteristics}"
                        )
                    elif len(all_child_facts) > 1:
                        raise ValueError(
                            f"Found more than one fact for concept {child_concept} with characteristics {parent_characteristics}"
                        )

                    child_fact = all_child_facts[0]

                    children_sum += child_fact.get_value_as_float() * child.get_weight()

                    if DEBUG:  # pragma: no cover
                        print(
                            f"+ {child_fact._get_id()}: {child_fact.get_value_as_float()} * {child.get_weight()}",
                            end=" ",
                        )

                if DEBUG:  # pragma: no cover
                    print()
                    print(f"node concept: {concept}, node value: {node_value}, children sum: {children_sum}")

                if node_value != children_sum:
                    return False

                # check the children
                for child in node.get_children():
                    child = cast(CalculationNetworkNode, child)
                    if not is_subnetwork_aggregation_consistent(child):
                        return False

            return True

        # check the roots
        for root in self.get_roots():
            root = cast(CalculationNetworkNode, root)
            if not is_subnetwork_aggregation_consistent(root):
                return False

        return True
