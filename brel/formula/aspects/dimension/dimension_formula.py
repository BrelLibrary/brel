from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.qnames.qname import QName


class DimensionFormula(AspectFormula):
    def __init__(self, dimension: QName):
        self.dimension: QName = dimension
        aspect = Aspect(dimension.clark_notation(), [])
        super().__init__(aspect)

    def get_dimension(self) -> QName:
        return self.dimension
