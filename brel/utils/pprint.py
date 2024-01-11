from brel.utils import (
    pprint_fact,
    pprint_facts,
    pprint_network,
    pprint_network_node,
)
from brel import Fact
from brel.networks import INetwork, INetworkNode


def pprint(to_print):
    """
    Pretty print the given object.
    Supports the following objects:
    - Fact
    - list[Fact]
    - INetwork
    - INetworkNode

    :param to_print: the object to pretty print
    :raises ValueError: if the given object is not supported
    """
    if isinstance(to_print, Fact):
        pprint_fact(to_print)
    elif isinstance(to_print, list):
        if len(to_print) > 0 and isinstance(to_print[0], Fact):
            pprint_facts(to_print)
        elif len(to_print) == 0:
            pprint_facts(to_print)
        else:
            raise ValueError("Can only pretty print lists of facts.")
    elif isinstance(to_print, INetwork):
        pprint_network(to_print)
    elif isinstance(to_print, INetworkNode):
        pprint_network_node(to_print)
    else:
        raise ValueError(
            f"Can only pretty print facts, lists of facts, networks and network nodes. Got {type(to_print)}"
        )
