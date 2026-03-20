from typing import Dict, List, Optional, Tuple

from brel.table_linkbases.parent_child_order import ParentChildOrder
from brel.table_linkbases.axis import Axis
from brel.table_linkbases.definition_model.breakdown import Breakdown
from brel.formula.filters.filter import Filter
from brel.table_linkbases.definition_model.parameter import Parameter


class Table:
    def __init__(
        self,
        linkrole: str,
        parent_child_order: ParentChildOrder,
        id: Optional[str],
        label: Optional[str],
    ):
        self.linkrole: str = linkrole
        self.parent_child_order = parent_child_order
        self.id = id
        self.label = label

        self.filters: List[Filter] = []
        self.parameters: List[Parameter] = []
        self.breakdowns: Dict[Axis, List[Tuple[Breakdown, int]]] = {
            Axis.X: [],
            Axis.Y: [],
            Axis.Z: [],
        }

    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def add_parameter(self, parameter: Parameter):
        self.parameters.append(parameter)

    def add_breakdown(self, axis: Axis, breakdown: Breakdown, order: int = 0):
        breakdown.set_axis(axis)
        self.breakdowns[axis].append((breakdown, order))

    def propagate_parent_child_order(self):
        if self.parent_child_order == ParentChildOrder.UNSPECIFIED:
            self.parent_child_order = ParentChildOrder.PARENT_FIRST

        for axis_breakdowns in self.breakdowns.values():
            for breakdown, _ in axis_breakdowns:
                breakdown.propagate_parent_child_order(self.parent_child_order)

    def get_linkrole(self) -> str:
        return self.linkrole
