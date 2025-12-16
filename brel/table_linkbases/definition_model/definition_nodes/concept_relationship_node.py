from typing import List, Optional
from brel.qnames.qname import QName
from brel.table_linkbases.definition_model.definition_nodes.relationship_node import (
    RelationshipNode,
)
from brel.table_linkbases.formula_axis import FormulaAxis
from brel.table_linkbases.parent_child_order import ParentChildOrder


class ConceptRelationshipNode(RelationshipNode):
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
        self.arcrole: Optional[str] = None
        self.linkname: Optional[QName] = None
        self.arcname: Optional[QName] = None

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

    def set_arcrole(self, arcrole: str):
        self.arcrole = arcrole

    def set_linkname(self, linkname: QName):
        self.linkname = linkname

    def set_arcname(self, arcname: QName):
        self.arcname = arcname
