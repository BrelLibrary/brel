from brel.resource import BrelReference


def test_reference():
    reference = BrelReference({"foo": "bar"}, "1234", "role")

    assert "foo" in str(reference), "Expected 'foo' to be in reference string"
    assert "bar" in str(reference), "Expected 'bar' to be in reference string"
    assert reference.get_label() == "1234", "Expected label to be '1234'"
    assert reference.get_role() == "role", "Expected role to be 'role'"
    assert reference.get_title() is None, "Expected title to be None. References do not have a title"
    assert reference.get_content() == {"foo": "bar"}, "Expected content to be {'foo': 'bar'}"
