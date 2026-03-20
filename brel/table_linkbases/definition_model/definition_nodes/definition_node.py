from abc import abstractmethod
from typing import List, Optional, Tuple

from brel.table_linkbases.parent_child_order import ParentChildOrder


class DefinitionNode:
    def __init__(
        self,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        self.tag_selector: Optional[str] = tag_selector
        self.id: Optional[str] = id
        self.label: Optional[str] = label

        self.order: float = 1
        self.children: List[Tuple[DefinitionNode, int]] = []

    def set_order(self, order: int):
        self.order = order

    def add_child(self, definition_node: "DefinitionNode", order: int = 0):
        self.children.append((definition_node, order))

    def propagate_parent_child_order(self, parent_child_order: ParentChildOrder):
        for definition_node, _ in self.children:
            definition_node.propagate_parent_child_order(parent_child_order)
