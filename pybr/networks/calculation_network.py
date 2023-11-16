import lxml
import lxml.etree

from pybr import QName
from pybr.networks import INetwork, CalculationNetworkNode
from pybr.reportelements import *

from typing import cast

class CalculationNetwork(INetwork):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a PyBRComponent.
    """
    # TODO: write docstrings
    def __init__(self, roots: list[CalculationNetworkNode], link_role: str, link_name: QName) -> None:
        self.__roots = roots
        self.__link_role = link_role
        self.__link_name = link_name
    
    # First class citizens
    def get_roots(self) -> list[CalculationNetworkNode]:
        """
        Get the root node of the presentation network
        @return: NetworkNode representing the root node of the network. Returns None if the network is empty.
        """
        return self.__roots

    def get_link_role(self) -> str:
        """
        Get the link role of the presentation network
        @return: str containing the link role of the network. 
        Note: This returns the same as get_URL() on the PyBRComponent
        """
        return self.__link_role

    def get_link_name(self) -> QName:
        return self.__link_name
    
    # second class citizens
    def validate(self, filing) -> bool:
        """
        Validate the presentation network against the PyBRFiling
        @param filing: PyBRFiling to validate against
        @return: bool indicating whether the presentation network is valid
        """
        # TODO: make nice
        def __validate_subtree(node: CalculationNetworkNode) -> bool:
            """
            Validate a subtree of the presentation network
            @param node: NetworkNode representing the root of the subtree
            @return: bool indicating whether the subtree is valid
            """
            # if the node has no children, then it is valid
            if len(node.get_children()) == 0:
                return True

            # validate the children
            for child in node.get_children():
                if not __validate_subtree(child):
                    return False
            
            # validate the node itself
            # get the report element
            concept = cast(PyBRConcept, node.get_report_element())

            # get the fact value associated with the concept
            facts = filing.get_facts_by_concept(concept)

            for fact in facts:
                fact_value = float(fact.get_value())

                children_aggregate = 0

                for child_node in node.get_children():
                    child_concept = cast(PyBRConcept, child_node.get_report_element())
                    child_facts = filing.get_facts_by_concept(child_concept)

                    # get the right fact by comparing the context
                    # TODO: currently just gets the right context by finding the one where the period is the same. Extend this to also check the entity, unit, etc.
                    child_fact = next(filter(lambda x: x.get_context() == fact.get_context(), child_facts), None)

                    child_fact_value = float(child_fact.get_value())
                    child_weight = float(child_node.get_weight())

                    children_aggregate += child_fact_value * child_weight
                
                if fact_value != children_aggregate:
                    return False
            
            return True
        
        return __validate_subtree(self.__roots)
                