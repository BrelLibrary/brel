from brel.networks import INetwork, INetworkNode

# from brel.utils import pprint
from functools import cmp_to_key


def nodes_equal(self: INetworkNode, other: INetworkNode) -> bool:
    # checks if two nodes have the same type and point to the same thing
    if not isinstance(other, INetworkNode):
        return False

    # two nodes are equal if they
    # 1. have the same type
    # 2. point to the same thing
    if type(self) != type(other):
        return False

    if self.points_to() != other.points_to():
        return False

    if self.points_to() == "resource":
        return self.get_resource() == other.get_resource()
    elif self.points_to() == "report element":
        return self.get_report_element() == other.get_report_element()
    elif self.points_to() == "fact":
        return self.get_fact() == other.get_fact()
    else:
        return False


def combine_networks(networks: list[INetwork]) -> INetwork:
    """
    Combine a list of networks into one network.
    This method destroys the original networks.
    :param networks: The networks to combine.
    :returns INetwork: The combined network.
    """
    if len(networks) == 0:
        raise ValueError("No networks provided.")

    # this algorithm works with the following steps:
    # 1. Get an order of the networks. Networks closer to the root come first.
    # 2. Create an empty aggregate network.
    # 3. For each network in the order, add the roots to the aggregate network nodes as children.

    if len(networks) == 1:
        return networks[0]

    # Step 1. sort the networks by prerequisite

    def is_prerequisite(n1: INetwork, n2: INetwork) -> int:
        # n1 is a prerequisite of n2 if all roots of n2 are in n1
        # and if the roots of n2 are not a subset of the roots of n1
        n1_roots = n1.get_roots()
        n2_roots = n2.get_roots()

        n1_nodes = n1.get_all_nodes()

        result = all((n2_root in n1_nodes for n2_root in n2_roots)) and not all(
            (n2_root in n1_roots for n2_root in n2_roots)
        )

        if result:
            return -1
        else:
            return 1

    networks_sorted = networks.copy()
    sorted(networks_sorted, key=cmp_to_key(is_prerequisite))

    # Step 2. Make an aggregate network.
    # In this case we re-use the first network as the aggregate network.
    agg_network = networks_sorted.pop()
    agg_roots = agg_network.get_roots()

    def get_all_nodes():
        all_nodes = []
        for root in agg_roots:
            all_nodes.extend(root.get_all_descendants())
        return all_nodes

    # Step 3. Add the roots of each network to the aggregate network.
    # if there is a node in the aggregate network that fits, then add the children of the root to that node.
    # otherwise, add the root to the aggregate networks roots.
    while len(networks_sorted) > 0:
        network = networks_sorted.pop()
        aggregate_nodes = get_all_nodes()
        for root in network.get_roots():
            parent = next((n for n in aggregate_nodes if nodes_equal(n, root)), None)
            if parent is None:
                agg_roots.append(root)
            else:
                for child in root.get_children():
                    parent._add_child(child)

    return agg_network
