from typing import List, Optional
from brel.characteristics.brel_aspect import Aspect
from brel.table_linkbases.definition_model.definition_nodes.open_definition_node import (
    OpenDefinitionNode,
)
from brel.formula.filters.filter import Filter


class AspectNode(OpenDefinitionNode):
    def __init__(
        self,
        participating_aspect: Aspect,
        include_unreported_value: bool,
        tag_selector: Optional[str],
        id: Optional[str],
        label: Optional[str],
    ):
        self.participating_aspect = participating_aspect
        self.include_unreported_value = include_unreported_value
        self.filters: List[Filter] = []
        super().__init__(tag_selector, id, label)

    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def get_participating_aspect(self):
        return self.participating_aspect

    def get_filters(self):
        return self.filters

    def get_include_unreported_value(self):
        return self.include_unreported_value
