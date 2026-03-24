from typing import List, Optional
from brel.qnames.qname import QName
from brel.table_linkbases.definition_model.definition_nodes.closed_definition_node import (
    ClosedDefinitionNode,
)
from brel.table_linkbases.formula_axis import FormulaAxis
from brel.table_linkbases.parent_child_order import ParentChildOrder


class RelationshipNode(ClosedDefinitionNode):
    def __init__(
        self,
        relationship_sources: List[QName | str],
        linkrole: str,
        formula_axis: FormulaAxis,
        generations: int,
        parent_child_order: ParentChildOrder,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        self.relationship_sources: List[QName | str] = relationship_sources
        self.linkrole: str = linkrole
        self.formula_axis: FormulaAxis = formula_axis
        self.generations: int = generations

        super().__init__(parent_child_order, tag_selector, id, label)
