from brel.characteristics import ExplicitDimensionCharacteristic, Aspect
from brel.reportelements import Dimension, Member
from brel import QName, QNameNSMap


def test_explicit_dimension():
    nsmap = QNameNSMap()
    dimension_name = QName("http://foo.com", "foo", "dim", nsmap)
    labels = []
    dimension = Dimension(dimension_name, labels)

    member_name = QName("http://foo.com", "foo", "mem", nsmap)
    member = Member(member_name, labels)

    aspect = Aspect(str(dimension_name), labels)

    characteristic = ExplicitDimensionCharacteristic(dimension, member, aspect)

    assert characteristic.get_aspect() == aspect, "Expected aspect to be aspect"
    assert characteristic.get_value() == member, "Expected value to be member"
    assert characteristic.get_dimension() == dimension, "Expected dimension to be dimension"

    assert str(member) in str(characteristic), "Expected member to be in characteristic string"

    assert characteristic == characteristic, "Expected characteristic to be equal to itself"
    assert characteristic != "foo", "Expected characteristic to not be equal to 'foo'"

    member_name2 = QName("http://foo.com", "foo", "mem2", nsmap)
    member2 = Member(member_name2, labels)

    characteristic2 = ExplicitDimensionCharacteristic(dimension, member2, aspect)

    assert characteristic != characteristic2, "Expected characteristic to not be equal to characteristic2"
