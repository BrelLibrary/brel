from typing import List, Optional

from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.filters.filter import Filter


class RuleSet:
    def __init__(self, tag: Optional[str] = None):
        self.rules: List[AspectFormula] = []
        self.tag: Optional[str] = tag

    def is_default(self):
        return self.tag is None

    def get_tag(self):
        return self.tag

    def get_rules(self):
        return self.rules

    def add_rule(self, rule: AspectFormula):
        self.rules.append(rule)
