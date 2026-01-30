from typing import Dict, Optional

from brel.table_linkbases.definition_model.definition_nodes.closed_definition_node import (
    ClosedDefinitionNode,
)
from brel.table_linkbases.definition_model.definition_nodes.rule_set import RuleSet
from brel.table_linkbases.parent_child_order import ParentChildOrder


class RuleNode(ClosedDefinitionNode):
    def __init__(
        self,
        is_abstract: bool,
        is_merge: bool,
        parent_child_order: ParentChildOrder,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        self.is_abstract = is_abstract
        self.is_merge = is_merge
        super().__init__(parent_child_order, tag_selector, id, label)

        self.rule_sets: Dict[Optional[str], RuleSet] = {}

    def add_rule_set(self, rule_set: RuleSet, tag: str) -> None:
        self.rule_sets[tag] = rule_set
