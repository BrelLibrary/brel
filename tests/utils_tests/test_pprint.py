import brel
import brel.utils


def test_pprint_BD():
    """
    Test if the pprint function fails for invalid inputs
    """

    # test if pprint does not work for a list of strings
    try:
        brel.utils.pprint(["a", "b", "c"])
        assert False, "Expected TypeError as input is not a Fact"
    except TypeError:
        pass

    # test that brel does not work for random objects
    try:
        brel.utils.pprint(1)
        assert False, "Expected TypeError as input is not a Fact"
    except TypeError:
        pass


def test_pprint_objects():
    """
    Test if the pprint function works for different objects
    """

    f = brel.Filing.open("tests/end_to_end_tests/ete_filing")
    fact = f.get_all_facts()[0]

    # test if pprint works for a fact
    try:
        brel.utils.pprint(fact)
    except:
        assert False, "pprint failed for a fact"

    # test if pprint works for a network
    network = f.get_all_physical_networks()[0]
    try:
        brel.utils.pprint(network)
    except:
        assert False, "pprint failed for a network"

    # test if pprint works for a network node
    node = network.get_roots()[0]
    try:
        brel.utils.pprint(node)
    except:
        assert False, "pprint failed for a network node"

    # test if it works for a component
    component = f.get_all_components()[0]
    try:
        brel.utils.pprint(component)
    except:
        assert False, "pprint failed for a component"


def test_pprint_lists():
    """
    Test if the pprint function works for lists of different objects
    """

    f = brel.Filing.open("tests/end_to_end_tests/ete_filing")

    # test if pprint works for a list of facts
    facts = f.get_all_facts()
    try:
        brel.utils.pprint(facts)
    except:
        assert False, "pprint failed for a list of facts"

    # test if pprint works for a list of components
    components = f.get_all_components()
    try:
        brel.utils.pprint(components)
    except:
        assert False, "pprint failed for a list of components"

    # test if it works for an empty list
    try:
        brel.utils.pprint([])
    except:
        assert False, "pprint failed for an empty list"
