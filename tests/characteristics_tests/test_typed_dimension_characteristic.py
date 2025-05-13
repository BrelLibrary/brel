"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""


from brel.characteristics import TypedDimensionCharacteristic, Aspect
from brel.reportelements import Dimension
from brel import QName
from brel.resource.brel_label import BrelLabel


def test_type_dimension():
    dimension_name = QName("http://foo.com", "foo", "dim")
    type_qname = QName("http://foo.com", "foo", "type")
    labels: list[BrelLabel] = []
    dimension = Dimension(dimension_name, "foo_dim", labels)
    dimension.make_typed(type_qname)

    aspect = Aspect(str(dimension_name), labels)

    value = "value"

    characteristic = TypedDimensionCharacteristic(dimension, value, aspect)

    assert characteristic.get_aspect() == aspect, "Expected aspect to be aspect"
    assert (
        characteristic.get_dimension() == dimension
    ), "Expected dimension to be dimension"
    assert characteristic.get_value() == "value", "Expected value to be 'value'"

    assert value in str(characteristic), "Expected value to be in characteristic string"

    # check equality
    characteristic2 = TypedDimensionCharacteristic(dimension, value + "2", aspect)
    assert (
        characteristic != characteristic2
    ), "Expected characteristic to not be equal to characteristic2"

    assert (
        characteristic == characteristic
    ), "Expected characteristic to be equal to itself"

    assert characteristic != "foo", "Expected characteristic to not be equal to 'foo'"
