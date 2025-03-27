"""
This module contains the pprint_network and pprint_network_node functions,
which can be used to print a brel network to the console.

====================

- author: Robin Schmidiger
- version: 0.8
- date: 21 January 2024

====================
"""

from brel.networks import *
from brel.reportelements import *
from brel.resource import *
from brel.resource import BrelLabel, BrelFootnote, BrelReference

ELBOW = "└──"
PIPE = "│  "
TEE = "├──"
SPACE = "   "

tag_lookup: dict[type, str] = {
    BrelLabel: "[LABEL]",
    BrelFootnote: "[FOOTNOTE]",
    BrelReference: "[REFERENCE]",
    Dimension: "[DIMENSION]",
    Member: "[MEMBER]",
    LineItems: "[LINE ITEMS]",
    Hypercube: "[HYPERCUBE]",
    Concept: "[CONCEPT]",
    Abstract: "[ABSTRACT]",
}

PADDING = max(map(lambda x: len(x), tag_lookup.values()))


def __print_sub_network(node: INetworkNode, last=True, header="") -> None:
    output_string = ""

    node_is_a = node.points_to()
    if node_is_a == "resource":
        resource = node.get_resource()
        type_str = ""
        if isinstance(resource, BrelLabel):
            label_role = resource.get_role()
            label_role_str = label_role.split("/")[-1]
            label_language = resource.get_language()
            label_content = resource.get_content()
            type_str = f"[{tag_lookup[BrelLabel]}] ({label_role_str} {label_language}) {label_content}"
        elif isinstance(resource, BrelReference):
            # type_str = f"[REFERENCE] {resource.get_content()}"
            role_str = resource.get_role().split("/")[-1]
            content = resource.get_content()
            type_str = f"[{tag_lookup[BrelReference]}] ({role_str}) {str(content)}"
        elif isinstance(resource, BrelFootnote):
            # type_str = "[RESOURCE]"
            role_tr = resource.get_role().split("/")[-1]
            text = resource.get_content()
            type_str = f"[{tag_lookup[BrelFootnote]}] ({role_tr}) {text}"

        output_string += type_str
    elif node_is_a == "report element":
        re = node.get_report_element()
        node_labels = re.get_labels()

        node_as_str = ""
        if hasattr(re, "get_preferred_label_role"):
            label_role = getattr(re, "get_preferred_label_role")()
            node_as_str = next(filter(lambda l: l.get_role() == label_role, node_labels)).get_content()
            node_as_str = str(node_as_str)
        else:
            node_as_str = str(re)

        type_str = ""
        if type(re) in tag_lookup:
            type_str = tag_lookup[type(re)]

        output_string += type_str + " " + node_as_str

    if hasattr(node, "get_weight"):
        weight = getattr(node, "get_weight")()
        weight_str = f"[W={weight:4}] "
    else:
        weight_str = ""

    # this adds some padding to the type header so that the node name is aligned
    if len(weight_str) != 0:
        padding_str = " " * (PADDING - len(weight_str))
    else:
        padding_str = ""

    output_string = weight_str + padding_str + output_string

    # issue: charmap codec can't encode character
    try:
        print(header + (ELBOW if last else TEE) + output_string)
    except UnicodeEncodeError:
        print((header + (ELBOW if last else TEE) + output_string).encode("utf-8"))
    children = node.get_children()
    for index, child in enumerate(children):
        is_last_child = index == len(children) - 1
        child_header = header + (SPACE if last else PIPE)
        __print_sub_network(child, is_last_child, child_header)


def pprint_network_node(node: INetworkNode):
    if node is None:
        return
    __print_sub_network(node)


def pprint_network(network: INetwork | None):
    if network is None:
        return

    print(f"Network (link role: {network.get_link_role()}), link name: {network.get_link_name()}")
    print(f"arc roles: {network.get_arc_roles()}, arc name: {network.get_arc_name()}")

    for index, root in enumerate(network.get_roots()):
        is_last_root = index == len(network.get_roots()) - 1
        __print_sub_network(root, is_last_root)
    print()
