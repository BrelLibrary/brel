"""
Tests for QName and QNameNSMap classes.

@author: Robin Schmidiger
@version: 0.1
@date: 22 December 2023
"""

from brel import QName, QNameNSMap


def create_empty_nsmap():
    return QNameNSMap()


def test_add_to_nsmap():
    """
    Tests the QNameNSMap.add_to_nsmap() method.
    Ties to achieve 100% branch coverage.
    """
    nsmap = create_empty_nsmap()

    def assert_valueerror(prefix, uri):
        try:
            nsmap.add_to_nsmap(uri, prefix)
            assert False
        except ValueError:
            pass

    # Try with a invalid None prefix
    assert_valueerror(None, "http://example.com")

    # run the method with a prefix that is not a string
    assert_valueerror(1, "http://example.com")

    # add a valid prefix
    nsmap.add_to_nsmap("http://example.com", "ns")
    assert nsmap.get_url("ns") == "http://example.com"

    # add the prefix again, but with a different uri
    assert_valueerror("ns", "http://example.org")

    # add the same url again but with a different prefix
    assert_valueerror("ns2", "http://example.com")
