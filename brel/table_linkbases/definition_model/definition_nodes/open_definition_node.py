from typing import Optional
from brel.table_linkbases.definition_model.definition_nodes.closed_definition_node import (
    ClosedDefinitionNode,
)
from brel.table_linkbases.definition_model.definition_nodes.definition_node import (
    DefinitionNode,
)
from brel.table_linkbases.parent_child_order import ParentChildOrder


class OpenDefinitionNode(DefinitionNode):
    def __init__(
        self,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        super().__init__(tag_selector, id, label)
