# Brel

Brel is a python library for XBRL.
It provides a simple API for extracting data from XBRL reports.

Brel stands for Business Report Extensible Library.

## Features

- [x] XBRL filings in XML format.
- [x] XBRL filings in XML format as zip files.
- [ ] XBRL filings in JSON format.
- [ ] XBRL filings in Inline XBRL format.
- [ ] XBRL filings in CSV format.
- [x] Resolve the Discoverable Taxonomy Set (DTS).
- [x] DTS caching.
- [x] Parse XBRL facts as python objects.
- [x] Parse XBRL networks as python objects.
- [x] Parse XBRL roles as python objects.


## Installation

To install Brel:

1. Clone the repository `git clone https://github.com/PapediPoo/Brel.git`
2. Change your working directory to the repository using `cd path/to/brel`
3. Run `python setup.py install` 

## Usage

### Importing
To use Brel, import the library and create a `Filing` using the `Filing.open` method:

```python
from brel import Filing, pprint_facts
filing = Filing.open("path/to/filing.zip")

# or

filing = Filing.open("path/to/filing.xml", "path/to/linkbase.xml")

# or

filing = Filing.open("path/to/filing/folder")
```

The `Filing` object provides access to everything in the filing, including the `Fact`s, `Component`s, 


### Facts

To print all the facts in the filing, use the `File.get_all_facts()` and `pprint_facts` functions:

```python
all_facts = filing.get_all_facts()
pprint_facts(all_facts)
```

since `Filing.get_all_facts()` returns a `list[Fact]`, we can iterate over it or use any standard list methods.

Assume you want to print all the facts in the filing where the Concept is "us-gaap:Assets".

```python
assets_concept = filing.get_concept("us-gaap:Assets")
if assets_concept is not None:
    assets_facts = filing.get_facts_by_concept(assets_concept)
    pprint_facts(assets_facts)
```

You could also use python's built-in `filter` function:
    
```python
assets_facts = filter(lambda fact: fact.get_concept() == assets_concept, all_facts)

# or

assets_facts = filter(lambda fact: str(fact.get_concept()) == "us-gaap:Assets", all_facts)
```

You can do the same for all the other aspects as well:

```python
# Gets all facts that report on the 31 Decemver 2018 and are in U.S Dollars.
usd_silvester_facts = filter(lambda fact: str(fact.get_unit()) == "usd" and str(fact.get_period()) == "on 2018-12-31", all_facts)
```

### Components/Components

Note: What brel calls 'Components', XBRL calls 'Roles'.

Components are what contains all the networks of a filing.

For example, to get the cover page component of a filing:

```python
cover_page = filing.get_component("http://foocompany.com/role/coverpage")

# in case you dont know the URI of the component, you can use the get_all_component_URIs method
component_uris = filing.get_all_component_URIs()
```

To get the presentation, calculation and definition networks of a component, use the `Component.get_presentation_network()`, `Component.get_calculation_network()` and `Component.get_definition_network()` methods respectively.
You can print them using the `pprint_network` function:

```python
presentation_network = cover_page.get_presentation_network()
calculation_network = cover_page.get_calculation_network()
definition_network = cover_page.get_definition_network()
pprint_network(presentation_network)
```

You can even navigate the networks yourself using the `Network.get_roots()` and `Node.get_children()` methods.
This code snippet gets the first child of all roots and prints the report element that the child points to:

```python

roots = presentation_network.get_roots()
for root in roots:
    first_child = root.get_children()[0]
    report_element = first_child.get_report_element()
    print(report_element)
```

Note: Network nodes can either point to Report Elements, Resources or Facts. Use the `Node.points_to` method to check what the node points to.

### Documentation

