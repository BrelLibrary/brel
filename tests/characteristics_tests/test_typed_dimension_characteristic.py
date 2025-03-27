from brel.characteristics import TypedDimensionCharacteristic, Aspect
from brel.reportelements import Dimension
from brel import QName, QNameNSMap


def test_type_dimension():
    nsmap = QNameNSMap()

    dimension_name = QName("http://foo.com", "foo", "dim", nsmap)
    type_qname = QName("http://foo.com", "foo", "type", nsmap)
    labels = []
    dimension = Dimension(dimension_name, labels)
    dimension.make_typed(type_qname)

    aspect = Aspect(str(dimension_name), labels)

    value = "value"

    characteristic = TypedDimensionCharacteristic(dimension, value, aspect)

    assert characteristic.get_aspect() == aspect, "Expected aspect to be aspect"
    assert characteristic.get_dimension() == dimension, "Expected dimension to be dimension"
    assert characteristic.get_value() == "value", "Expected value to be 'value'"

    assert value in str(characteristic), "Expected value to be in characteristic string"

    # check equality
    characteristic2 = TypedDimensionCharacteristic(dimension, value + "2", aspect)
    assert characteristic != characteristic2, "Expected characteristic to not be equal to characteristic2"

    assert characteristic == characteristic, "Expected characteristic to be equal to itself"

    assert characteristic != "foo", "Expected characteristic to not be equal to 'foo'"
