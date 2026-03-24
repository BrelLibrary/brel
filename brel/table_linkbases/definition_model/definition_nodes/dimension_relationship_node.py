from typing import List, Optional
from brel.qnames.qname import QName
from brel.reportelements.dimension import Dimension
from brel.table_linkbases.definition_model.definition_nodes.relationship_node import (
    RelationshipNode,
)
from brel.table_linkbases.formula_axis import FormulaAxis
from brel.table_linkbases.parent_child_order import ParentChildOrder


class DimensionRelationshipNode(RelationshipNode):
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
        self.dimension: Optional[Dimension] = None
        super().__init__(
            relationship_sources,
            linkrole,
            formula_axis,
            generations,
            parent_child_order,
            tag_selector,
            id,
            label,
        )

    def set_dimension(self, dimension: Dimension):
        self.dimension = dimension

    def get_dimension(self) -> Dimension:
        if self.dimension is None:
            raise ValueError("Dimension is not set")

        return self.dimension
