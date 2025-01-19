from brel.resource import BrelLabel


def test_label():
    label = BrelLabel("text", "1234", "lang", "role")

    assert "text" in str(label), "Expected 'text' to be in label string"
    assert label.get_language() == "lang", "Expected language to be 'lang'"
    assert label.get_label_role() == "role", "Expected role to be 'role'"
    assert label.get_label() == "1234", "Expected label to be '1234'"
    assert label.get_title() is None, "Expected title to be None. Labels do not have a title"
    assert label.get_content() == "text", "Expected content to be 'text'"
