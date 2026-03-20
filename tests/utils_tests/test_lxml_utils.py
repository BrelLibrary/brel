from lxml import etree

from brel.parsers.utils.lxml_utils import get_all_nsmaps, get_str_attribute


def test_get_str():
    # make the element <foo bar="1"/>
    element = etree.Element("foo")
    element.set("bar", "1")

    assert get_str_attribute(element, "bar") == "1", "Expected bar to be 1"
    assert get_str_attribute(element, "foo", "2") == "2", "Expected foo to be 2"

    try:
        get_str_attribute(element, "baz")
        assert False, "Expected get_str to raise an error"
    except ValueError:
        pass


def test_get_all_nsmaps():
    element1_str = "<foo xmlns:foo='http://www.foo.com'/>"
    element1 = etree.fromstring(element1_str)

    element2_str = "<bar xmlns:bar='http://www.bar.com'/>"
    element2 = etree.fromstring(element2_str)

    nsmaps = get_all_nsmaps([element1, element2])
    assert any(
        "foo" in nsmap for nsmap in nsmaps
    ), "Expected 'foo' to be in one of the nsmaps"
    assert any(
        "bar" in nsmap for nsmap in nsmaps
    ), "Expected 'bar' to be in one of the nsmaps"
