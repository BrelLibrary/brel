"""
Module for pretty printing the most common Brel objects to the console.
Acts as a wrapper around the other pretty print functions and automatically selects the correct one based on the given object.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 03 February 2024

====================
"""

from brel import Fact, Component
from brel.networks import INetwork, INetworkNode
from brel.utils import (
    pprint_fact,
    pprint_facts,
    pprint_network,
    pprint_network_node,
    pprint_component,
)


def pprint(to_print):
    """
    Pretty print the given object.
    Supports the following objects:
    - Fact
    - list[Fact]
    - INetwork
    - INetworkNode
    - Component

    :param to_print: the object to pretty print
    :raises ValueError: if the given object is not supported
    """
    if isinstance(to_print, Fact):
        pprint_fact(to_print)
    elif isinstance(to_print, list):
        if len(to_print) == 0:
            pprint_facts(to_print)
        elif isinstance(to_print[0], Fact):
            pprint_facts(to_print)
        elif isinstance(to_print[0], Component):
            for component in to_print:
                pprint_component(component)
        else:
            raise TypeError("Can only pretty print lists of facts.")
    elif isinstance(to_print, INetwork):
        pprint_network(to_print)
    elif isinstance(to_print, INetworkNode):
        pprint_network_node(to_print)
    elif isinstance(to_print, Component):
        pprint_component(to_print)
    else:
        raise TypeError(
            f"Can only pretty print facts, lists of facts, components, networks and network nodes. Got {type(to_print)}"
        )
