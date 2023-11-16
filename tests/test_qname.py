from pybr.qname import QName
from pytest import raises

def test_qname_init():
    
    # test with unknown namespace
    qn = QName("http://example.com/ns0", "ns0", "foo")
    assert qn.get_URL() == "http://example.com/ns0"
    assert qn.get_local_name() == "foo"
    assert qn.get_prefix() == "ns0"
    assert qn.get() == "ns0:foo"
    assert qn.resolve() == "{http://example.com/ns0}foo"
    assert qn.__str__() == "ns0:foo"

    # test with known namespace
    qn = QName("http://example.com/ns0", "ns0", "bar")
    assert qn.get_URL() == "http://example.com/ns0"
    assert qn.get_local_name() == "bar"
    assert qn.get_prefix() == "ns0"
    assert qn.get() == "ns0:bar"
    assert qn.resolve() == "{http://example.com/ns0}bar"
    assert qn.__str__() == "ns0:bar"

def test_qname_eq():
    # test if both QNames are equal
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    qn2 = QName("http://example.com/ns0", "ns0", "foo")
    assert qn1 == qn2

    # test if both QNames have different URLs
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    qn2 = QName("http://example.com/ns1", "ns1", "foo")
    assert qn1 != qn2

    # test if both QNames have different local names
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    qn2 = QName("http://example.com/ns0", "ns0", "bar")
    assert qn1 != qn2

    # test if one is not a QName
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    assert qn1 != "foo"

def test_qname_hash():
    # test hash equality
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    qn2 = QName("http://example.com/ns0", "ns0", "foo")
    assert hash(qn1) == hash(qn2)

    # test hash inequality
    qn1 = QName("http://example.com/ns0", "ns0", "foo")
    qn2 = QName("http://example.com/ns0", "ns0", "bar")
    assert hash(qn1) != hash(qn2)

def test_qname_from_string():
    # first populate the namespace cache
    QName("http://example.com/ns0", "ns0", "foo")

    # test with known namespace.
    # the qname string is "{url}localname"
    qn = QName.from_string("{http://example.com/ns0}bar")
    assert qn.get_URL() == "http://example.com/ns0"
    assert qn.get_local_name() == "bar"
    assert qn.get_prefix() == "ns0"

    # test with unknown namespace
    # the qname string is "prefix:localname"
    qn = QName.from_string("ns0:bar")
    assert qn.get_URL() == "http://example.com/ns0"
    assert qn.get_local_name() == "bar"
    assert qn.get_prefix() == "ns0"

    # test with unknown namespace
    # the qname string is "{url}localname"
    raises(ValueError, QName.from_string, "{http://example.com/nsunknown}bar")

    # test with unknown namespace
    # the qname string is "prefix:localname"
    raises(ValueError, QName.from_string, "nsunknown:bar")

    # test invalid qname strings
    raises(ValueError, QName.from_string, "ns1bar")
    raises(ValueError, QName.from_string, "ns1:bar:baz")
    raises(ValueError, QName.from_string, "{http://example.com/ns1}bar:baz")
    raises(ValueError, QName.from_string, "{http://example.com/ns1}bar:baz:qux")
    raises(ValueError, QName.from_string, "{http://example.com/ns1{bar")
    raises(ValueError, QName.from_string, "}http://example.com/ns1}bar}")
    raises(ValueError, QName.from_string, "{http://example}bar")

def test_qname_nsmap():
    # test if arbitrary namespace is not in nsmap
    nsmap = QName.get_nsmap()

    assert "unknown" not in nsmap

    # test if known namespace is in nsmap
    QName("http://example.com/ns0", "ns0", "foo")
    nsmap = QName.get_nsmap()
    assert "ns0" in nsmap
    assert nsmap["ns0"] == "http://example.com/ns0"

    # test if namespace can be added to nsmap using add_to_nsmap
    QName.add_to_nsmap("http://example.com/ns1", "ns1")
    nsmap = QName.get_nsmap()
    assert "ns1" in nsmap
    assert nsmap["ns1"] == "http://example.com/ns1"

    # try to add None prefix to nsmap
    raises(ValueError, QName.add_to_nsmap, "http://example.com/ns1", None) 

    # test if invalid an invalid url cannot be added to nsmap
    raises(ValueError, QName.add_to_nsmap, "http://example", "ns2")

    # test if nsmap enforces 1:1 mapping. So prefixes cannot map to existing urls and vice versa
    raises(ValueError, QName.add_to_nsmap, "http://example.com/nsunknown", "ns1")
    raises(ValueError, QName.add_to_nsmap, "http://example.com/ns1", "unknown")

def test_qname_is_str_qname():
    qn1 = QName("http://example.com/ns0", "ns0", "foo")

    assert QName.is_str_qname(qn1)
    assert QName.is_str_qname("ns0:foo")
    assert not QName.is_str_qname("foo")
    assert not QName.is_str_qname(1)

def test_qname_ns_cache():
    qn1 = QName("http://example.com/ns1", "ns1", "foo")
    qn2 = QName.from_string("ns1:foo")
    assert qn1 == qn2

def test_qname_try_get_prefix():
    # try with invalid url
    assert QName.try_get_prefix_from_url("http://example") is None

    # add prefix to nsmap
    QName.add_to_nsmap("http://example.com/ns0", "ns0")

    # try with prefix in nsmap
    assert QName.try_get_prefix_from_url("http://example.com/ns0") == "ns0"

    # try with url where the last part is not a number
    assert QName.try_get_prefix_from_url("http://example.com/nstry") == "nstry"

    # try with url where the last part is a number
    assert QName.try_get_prefix_from_url("http://example.com/nstry/1") == "nstry"

    # try with url where there is no last part, only the domain
    assert QName.try_get_prefix_from_url("http://example.com") is None

    # try with url where the last part is a number
    assert QName.try_get_prefix_from_url("http://example.com/1") is None

    # try with empty string
    assert QName.try_get_prefix_from_url("") is None

