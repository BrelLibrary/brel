from pybr.networks import PresentationNetwork, NetworkNode
from pybr.reportelements import *

def pprint_network(network: PresentationNetwork | None) -> None:
    """
    Pretty print a presentation network
    @param network: PresentationNetwork to be pretty printed
    @return: None
    """
    if network is None:
        return

    print(f"Presentation network (link role: {network.get_link_role()}")
    pprint_network_node(network.get_root(), True)


def pprint_network_node(node: NetworkNode | None, print_report_element_type=False) -> None:
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

        type_header = ""

        if print_report_element_type:
            if isinstance(node.get_report_element(), PyBRDimension):
                type_header = "[DIMENSION]"
            elif isinstance(node.get_report_element(), PyBRMember):
                type_header = "[MEMBER]"
            elif isinstance(node.get_report_element(), PyBRLineItems):
                type_header = "[LINE ITEMS]"
            elif isinstance(node.get_report_element(), PyBRHypercube):
                type_header = "[HYPERCUBE]"
            elif isinstance(node.get_report_element(), PyBRConcept):
                type_header = "[CONCEPT]"
            elif isinstance(node.get_report_element(), PyBRAbstract):
                type_header = "[ABSTRACT]"
        
            # this adds some padding to the type header so that the node name is aligned
            padding = 12  # TODO: maybe not hardcode this
            type_header = type_header + " " * (padding - len(type_header))

        print(header + (elbow if last else tee) + type_header + node_as_str)
        children = node.get_children()
        for index, child in enumerate(children):
            is_last_child = index == len(children) - 1
            child_header = header + (space if last else pipe)
            __print_subnetwork(child, is_last_child, child_header)
        

    if node is None:
        return
    __print_subnetwork(node)
