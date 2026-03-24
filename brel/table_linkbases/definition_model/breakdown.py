from collections import OrderedDict
from typing import List, Optional, Tuple

from brel.table_linkbases.definition_model.definition_nodes.definition_node import (
    DefinitionNode,
)
from brel.table_linkbases.parent_child_order import ParentChildOrder
from brel.table_linkbases.axis import Axis


class Breakdown:
    def __init__(
        self,
        parent_child_order: ParentChildOrder,
        id: Optional[str],
        label: Optional[str],
    ):
        self.parent_child_order = parent_child_order
        self.id = id
        self.label = label

        self.axis = Axis.X
        self.roots: List[Tuple[DefinitionNode, int]] = []

    def set_axis(self, axis: Axis):
        self.axis = axis

    def add_root(self, definition_node: DefinitionNode, order: int):
        self.roots.append((definition_node, order))

    def propagate_parent_child_order(self, parent_child_order: ParentChildOrder):
        if self.parent_child_order == ParentChildOrder.UNSPECIFIED:
            self.parent_child_order = parent_child_order

        for definition_node, _ in self.roots:
            definition_node.propagate_parent_child_order(self.parent_child_order)
