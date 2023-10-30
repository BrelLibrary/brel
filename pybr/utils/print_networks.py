from pybr.networks import PresentationNetwork, NetworkNode

def pprint_network(network: PresentationNetwork | None) -> None:
    """
    Pretty print a presentation network
    @param network: PresentationNetwork to be pretty printed
    @return: None
    """
    if network is None:
        return

    print(f"Presentation network (link role: {network.get_link_role()}")
    pprint_network_node(network.get_root())


def pprint_network_node(node: NetworkNode | None) -> None:
    """
    Pretty print a network node
    @param node: NetworkNode to be pretty printed
    @return: None
    """
    elbow = "└──"
    pipe  = "│  "
    tee   = "├──"
    space = "   "

    def __print_subnetwork(node: NetworkNode, last=True, header='') -> None:
        node_preferred_label_role = node.preferred_label_role()
        node_labels = node.get_report_element().get_labels()
        node_preferred_label = filter(lambda label: label.get_role() == node_preferred_label_role, node_labels).__next__()
        node_as_str = str(node_preferred_label)
        print(header + (elbow if last else tee) + node_as_str)
        children = node.get_children()
        for index, child in enumerate(children):
            is_last_child = index == len(children) - 1
            child_header = header + (space if last else pipe)
            __print_subnetwork(child, is_last_child, child_header)
        

    if node is None:
        return
    __print_subnetwork(node)
