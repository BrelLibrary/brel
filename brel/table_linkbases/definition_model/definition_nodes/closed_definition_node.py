from typing import Optional, override
from brel.table_linkbases.definition_model.definition_nodes.definition_node import (
    DefinitionNode,
)
from brel.table_linkbases.parent_child_order import ParentChildOrder


class ClosedDefinitionNode(DefinitionNode):
    def __init__(
        self,
        parent_child_order: ParentChildOrder,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        self.parent_child_order = parent_child_order
        super().__init__(tag_selector, id, label)

    @override
    def propagate_parent_child_order(self, parent_child_order: ParentChildOrder):
        if self.parent_child_order == ParentChildOrder.UNSPECIFIED:
            self.parent_child_order = parent_child_order

        for definition_node, _ in self.children:
            definition_node.propagate_parent_child_order(self.parent_child_order)
