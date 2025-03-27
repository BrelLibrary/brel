from brel.resource import BrelFootnote


def test_footnote():
    footnote = BrelFootnote("text", "1234", "lang", "role")

    assert "text" in str(footnote), "Expected 'text' to be in footnote string"
    assert footnote.get_language() == "lang", "Expected language to be 'lang'"
    assert footnote.get_role() == "role", "Expected role to be 'role'"
    assert footnote.get_label() == "1234", "Expected label to be '1234'"
    assert footnote.get_title() is None, "Expected title to be None. Footnotes do not have a title"
    assert footnote.get_content() == "text", "Expected content to be 'text'"
