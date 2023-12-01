from pybr.networks import *
from pybr.reportelements import *
from pybr import BrelLabelRole

ELBOW = "└──"
PIPE  = "│  "
TEE   = "├──"
SPACE = "   "

def __print_subnetwork(node: INetworkNode, last=True, header='') -> None:
    report_element = node.get_report_element()
    node_labels = report_element.get_labels()

    if hasattr(report_element, "get_preferred_label_role"):
        label_role = getattr(report_element, "get_preferred_label_role")()
    else:
        label_role = BrelLabelRole.STANDARD_LABEL
    
    node_preferred_label = next(filter(lambda label: label.get_label_role() == label_role, node_labels), str(report_element.get_name()))
    node_as_str = str(node_preferred_label)

    type_str = ""
    if isinstance(node.get_report_element(), PyBRDimension):
        type_str = "[DIMENSION]"
    elif isinstance(node.get_report_element(), PyBRMember):
        type_str = "[MEMBER]"
    elif isinstance(node.get_report_element(), PyBRLineItems):
        type_str = "[LINE ITEMS]"
    elif isinstance(node.get_report_element(), PyBRHypercube):
        type_str = "[HYPERCUBE]"
    elif isinstance(node.get_report_element(), PyBRConcept):
        type_str = "[CONCEPT]"
    elif isinstance(node.get_report_element(), PyBRAbstract):
        type_str = "[ABSTRACT]"
    
    if hasattr(node, "get_weight"):
        weight = getattr(node, "get_weight")()
        weight_str = f"[W={weight:4}] "
    else:
        weight_str = ""

    # this adds some padding to the type header so that the node name is aligned
    padding = 14  # TODO: maybe not hardcode this
    padding_str = " " * (padding - len(weight_str))
    
    print(header + (ELBOW if last else TEE) + type_str + weight_str + padding_str + node_as_str)
    children = node.get_children()
    for index, child in enumerate(children):
        is_last_child = index == len(children) - 1
        child_header = header + (SPACE if last else PIPE)
        __print_subnetwork(child, is_last_child, child_header)

def pprint_network_node(node: INetworkNode):
    
    if node is None:
        return
    __print_subnetwork(node)

def pprint_network(network: INetwork | None):
    if network is None:
        return
    
    print(f"Network (link role: {network.get_link_role()}), link name: {network.get_link_name()}")
    print(f"arc roles: {network.get_arc_roles()}, arc name: {network.get_arc_name()}")
    
    for index, root in enumerate(network.get_roots()):
        is_last_root = index == len(network.get_roots()) - 1
        __print_subnetwork(root, is_last_root)
    print()
