from pybr.networks import *
from pybr.reportelements import *
from pybr import PyBRLabelRole

def pprint_presentation_network(network: PresentationNetwork | None, label_role: PyBRLabelRole | None = None, print_report_element_type=False) -> None:
    """
    Pretty print a presentation network
    @param network: PresentationNetwork to be pretty printed
    @return: None
    """
    # TODO: think about the optional args again
    if network is None:
        return

    print(f"Presentation network (link role: {network.get_link_role()}")
    pprint_presentation_network_node(network.get_root(), label_role=label_role, print_report_element_type=print_report_element_type)


def pprint_presentation_network_node(node: PresentationNetworkNode | None, label_role: PyBRLabelRole | None = None, print_report_element_type=False) -> None:
    """
    Pretty print a network node
    @param node: NetworkNode to be pretty printed
    @param label_role: PyBRLabelRole to be used for printing the node. If None, the node's preferred label role is used
    @param print_report_element_type: bool indicating whether or not to print the type of the report element e.g. [DIMENSION] or [MEMBER]
    @return: None
    """
    # TODO: think about the optional args again

    elbow = "└──"
    pipe  = "│  "
    tee   = "├──"
    space = "   "

    def __print_subnetwork(node: PresentationNetworkNode, last=True, header='') -> None:
        if label_role is None:
            node_preferred_label_role = node.get_preferred_label_role()
        else:
            node_preferred_label_role = label_role
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
            padding = 14  # TODO: maybe not hardcode this
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


def pprint_calculation_network(network: CalculationNetwork | None, label_role: PyBRLabelRole = PyBRLabelRole.STANDARD_LABEL) -> None:
    """
    Pretty print a calculation network
    @param network: CalculationNetwork to be pretty printed
    @return: None
    """
    # TODO: think about the optional args again
    if network is None:
        return

    print(f"Calculation network (link role: {network.get_link_role()}")
    for root in network.get_roots():
        pprint_calculation_network_node(root, label_role=label_role)
        print()


def pprint_calculation_network_node(node: CalculationNetworkNode | None, label_role: PyBRLabelRole = PyBRLabelRole.STANDARD_LABEL) -> None:
    """
    Pretty print a network node
    @param node: NetworkNode to be pretty printed
    @param label_role: PyBRLabelRole to be used for printing the node. If None, the node's preferred label role is used
    @param print_report_element_type: bool indicating whether or not to print the type of the report element e.g. [DIMENSION] or [MEMBER]
    @return: None
    """

    elbow = "└──"
    pipe  = "│  "
    tee   = "├──"
    space = "   "

    def __print_subnetwork(node: CalculationNetworkNode, last=True, header='') -> None:
        node_labels = node.get_report_element().get_labels()
        node_preferred_label = filter(lambda label: label.get_role() == label_role, node_labels).__next__()
        node_as_str = str(node_preferred_label)
        # node_as_str = str(node.get_report_element().get_name())
        node_weight = node.get_weight()

        # type_header = str(node_weight)
        type_header = f"[{node_weight:4}] "
        
        print(header + (elbow if last else tee) + type_header + node_as_str)
        children = node.get_children()
        for index, child in enumerate(children):
            is_last_child = index == len(children) - 1
            child_header = header + (space if last else pipe)
            __print_subnetwork(child, is_last_child, child_header)
    
    if node is None:
        return
    __print_subnetwork(node)


def pprint_definition_network(network: DefinitionNetwork | None, label_role: PyBRLabelRole | None = None, print_report_element_type=False) -> None:
    """
    Pretty print a presentation network
    @param network: PresentationNetwork to be pretty printed
    @return: None
    """
    # TODO: think about the optional args again
    if network is None:
        return

    print(f"Presentation network (link role: {network.get_link_role()}")
    pprint_definition_network_node(network.get_root(), label_role=label_role, print_report_element_type=print_report_element_type)


def pprint_definition_network_node(node: DefinitionNetworkNode | None, label_role: PyBRLabelRole | None = None, print_report_element_type=False) -> None:
    """
    Pretty print a network node
    @param node: NetworkNode to be pretty printed
    @param label_role: PyBRLabelRole to be used for printing the node. If None, the node's preferred label role is used
    @param print_report_element_type: bool indicating whether or not to print the type of the report element e.g. [DIMENSION] or [MEMBER]
    @return: None
    """
    # TODO: think about the optional args again

    elbow = "└──"
    pipe  = "│  "
    tee   = "├──"
    space = "   "

    def __print_subnetwork(node: DefinitionNetworkNode, last=True, header='') -> None:
        if label_role is None:
            node_preferred_label_role = PyBRLabelRole.STANDARD_LABEL
        else:
            node_preferred_label_role = label_role
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
            padding = 14  # TODO: maybe not hardcode this
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

def pprint_network_node(node: INetworkNode):
    elbow = "└──"
    pipe  = "│  "
    tee   = "├──"
    space = "   "

    def __print_subnetwork(node: INetworkNode, last=True, header='') -> None:
        report_element = node.get_report_element()
        node_labels = report_element.get_labels()

        if hasattr(report_element, "get_preferred_label_role"):
            label_role = getattr(report_element, "get_preferred_label_role")()
        else:
            label_role = PyBRLabelRole.STANDARD_LABEL
        
        node_preferred_label = next(filter(lambda label: label.get_role() == label_role, node_labels), str(report_element.get_name()))
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
        
        print(header + (elbow if last else tee) + type_str + weight_str + padding_str + node_as_str)
        children = node.get_children()
        for index, child in enumerate(children):
            is_last_child = index == len(children) - 1
            child_header = header + (space if last else pipe)
            __print_subnetwork(child, is_last_child, child_header)
    
    if node is None:
        return
    __print_subnetwork(node)

def pprint_network(network: INetwork | None):
    if network is None:
        return

    print(f"Network (link role: {network.get_link_role()}), link name: {network.get_link_name()}")
    for root in network.get_roots():
        pprint_network_node(root)
        print()
