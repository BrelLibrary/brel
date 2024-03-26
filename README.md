# Brel

Brel is a Python library for reading and analyzing financial reports, such as balance sheets, income statements, cash flow statements, as well as sustainability repots.

## A bit of history and context

Accounting has existed for thousands of years. Until 20 years ago, most reports were simply printed and distributed in books, or shared as PDF files. Many countries require that public companies listed on stock exchanges submit such quarterly financial reports including among others a balance sheet, an income statement, a cash flow statement.

Around 15 years ago, some authorities (in the U.S., in Japan) started requesting that these reports be submitted in a machine-readable format. A very large number of countries then followed, and the standard commonly adopted for machine readability is XBRL, which stands for eXtensible Business Reporting Language.

XBRL reports are based on a data cube model, where each piece of data (called fact) is submitted with dimensions (e.g., Assets, for Coca Cola, fiscal year 2023, in USD). The facts are then organized in cubes called components (balance sheet, income statement, etc) and can be presented to the user in a format similar to what accountants are used to, with hierarchies of line items (assets, liabilities, equity, profit/loss, revenue, etc). The metadata is taxonomy-oriented, meaning that a report is accompanied with a list of concepts to report, together with references to legal documentation, translation in multiple languages, calculation and validation rules, etc. This makes the standard robust, professional. More recently, it has become common to neatly nest ("tag") the facts inside fancy-looking HTML documents, but the data model remains the same.

One of the immediate benefits of machine-readable formats is that most authorities are now able to immediately reject reports containing validation errors on their submission portal (e.g., EDGAR for the U.S. Securities and Exchange Commission), while it used to be weeks or months for doing so as it was done by humans.

Another benefit is that analysts can open the reports and analyse with their favorite Data Science libraries and database systems.

## The Brel API

It is often heard that XBRL is complicated, because the syntax involves some complex XML. But did you know that Excel and Word files do as well involve complex XML? Yet most people are not aware of this, because they use the fancy Excel and Word user interfaces. The same goes with XBRL: while the ecosystem is still being developed, XBRL users should work with a higher-level, logical view; this idea was called Data Independence by Edgar Codd in 1970, when relational databases were designed.

Brel provides a simple API for extracting data from XBRL reports with Python, respects the Open Information Model, follows Charles Hoffman's vision on XBRL, understands dimensions and cubes, and shields you from the XML syntax.

Brel is not a UI, it is an API. But it is designed in such a way that UIs can be built on top of its API.

It is being developed at ETH Zurich by Robin Schmidiger in a Master's thesis supervised by Ghislain Fourny.

Its installation and use is straightforward as it is available as a pip package.

Very important: this is an early version still under development, there will be bugs! At this stage we warmly welcome feedback and bug reports. For the moment, we focus on reports with open taxonomies: SEC's EDGAR filings, European Single Electronic Format (ESEF), etc. The Data Point Model (DPM, used by the European Banking Authority) will be supported in a later stage.

Brel stands for Business Report Extensible Library.

### Documentation

The documentation of the Brel API is available on GitHub Pages [here](https://brellibrary.github.io/brel/). Below we give a few examples to get you started.

## (Un)implemented features

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

`pip install brel-xbrl`

## Usage

### Importing
To use Brel, import the library and create a `Filing` using the `Filing.open` method.

```python
from brel import Filing, pprint
filing = Filing.open("path/to/filing.zip")

# or 

filing = Filing.open("https://uri.to.filing.xml")

# or

filing = Filing.open("path/to/filing/folder")
```

If you have a report from the SEC's EDGAR database, you can use the `open_edgar` function to load the filing. This function allows you to load filings by specifying the company's CIK, the form type, and the date of the filing.

```python

from brel import Filing
from brel.utils import open_edgar, pprint

# Loads Apples 10-Q filing from Q4 2023
filing = open_edgar(cik="320193", filing_type="10-Q", date="2023-12-30")

# or 

filing = open_edgar(cik="320193", filing_type="10-Q")  # opens latest filing
```

The `Filing` object provides access to everything in the filing, including the `Fact`s, `Component`s, 

If you do not have a report, you could for example download all the files under "Data Files" of the [latest annual report (10-K) by Apple](https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/0000320193-23-000106-index.htm) into a folder, and then pass this folder to Filing.open():

```python
from brel import Filing, pprint
filing = Filing.open("path/to/aapl-20220924_htm.xml")
```
	 
### Facts

To print all the facts in the filing and print a list of facts, use the `File.get_all_facts()` and `pprint` functions:

Note that printing all the will give you a lot of output, so it is recommended to print only a few facts.

```python
all_facts = filing.get_all_facts()
first_10_facts = all_facts[:10]
pprint(first_10_facts)
```

since `Filing.get_all_facts()` returns a `list[Fact]`, we can iterate over it or use any standard list methods.

Assume you want to print all the facts in the filing where the Concept is "us-gaap:Assets".

```python
assets_concept = filing.get_concept("us-gaap:Assets")
if assets_concept is not None:
    assets_facts = filing.get_facts_by_concept(assets_concept)
    pprint(assets_facts)
```
<!-- 
The object `assets_concept` is a `Concept` object that represents the concept "us-gaap:Assets".
It contains all the information about the concept, including its name, its labels, its type, etc. -->

You could also use python's built-in `filter` function:
    
```python
assets_facts = list(
    filter(lambda fact: fact.get_concept().get_value() == assets_concept, all_facts)
)
# or

assets_facts = list(
    filter(
        lambda fact: str(fact.get_concept()) == "us-gaap:Assets", all_facts
    )
)
```

You can do the same for all the other aspects as well:

```python
# Gets all facts that report on the 31 Decemver 2018 and are in U.S Dollars.
usd_silvester_facts = list(
    filter(
        lambda fact: str(fact.get_unit()) == "usd"
        and str(fact.get_period()) == "on 2018-12-31",
        all_facts,
    )
)
```

### Components/Components

Note: What brel calls 'Components', XBRL calls 'Roles'.

Components are what contains all the networks of a filing.

For example, to get the cover page component of a filing:

```python
cover_page = filing.get_component("http://foocompany.com/role/coverpage")

# in case you dont know the URI of the component, you can use the get_all_component_uris method
component_uris = filing.get_all_component_uris()
print(component_uris)

```

To get the presentation, calculation and definition networks of a component, use the `Component.get_presentation_network()`, `Component.get_calculation_network()` and `Component.get_definition_network()` methods respectively.
You can print them using the same `pprint` function as before:

```python
# Get all the networks of the cover page component
presentation_network = cover_page.get_presentation_network()
calculation_network = cover_page.get_calculation_network()
definition_network = cover_page.get_definition_network()

# If they exist, print them
if presentation_network is not None:
    pprint(presentation_network)
if calculation_network is not None:
    pprint(calculation_network)
if definition_network is not None:
    pprint(definition_network)
```
```

You can even navigate the networks yourself using the `Network.get_roots()` and `Node.get_children()` methods.
This code snipped prints the first child of the first root of the presentation network:

```python

roots = presentation_network.get_roots()
first_root = roots[0]
first_root_children = first_root.get_children()
first_child = first_root_children[0]

pprint(first_child)
```

Note: Network nodes can either point to Report Elements, Resources or Facts. Use the `Node.points_to` method to check what the node points to.

### Credits

Brel is available with an Apache License 2.0 license.

© 2023-2024 Robin Schmidiger, Ghislain Fourny, Gustavo Alonso
