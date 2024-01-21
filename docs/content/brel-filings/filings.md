<a id="brel.brel_filing"></a>

# brel.brel\_filing

Brel operates on XBRL filings and represents them as a [`Filing`](#brel.brel_filing.Filing) object.
This module contains the Filing class.

Filings can be loaded from a folder, a zip file, or one or multiple xml files.

- If a folder is given, then all xml files in the folder are loaded.
- If a zip file is given, then the zip file is extracted to a folder 
and then all xml files in the folder are loaded.
- If one or more xml files are given, then only those xml files are loaded.

Example usage:

```
from brel import Filing

# open the filing
filing1 = Filing.open("my_filing.zip")

filing2 = Filing.open("my_folder/")

filing3 = Filing.open("my_file.xml", "my_file2.xml")

# get the facts reporting agains us-gaap:Assets
assets_facts = filing1.get_facts_by_concept_name("us-gaap:Assets")
pprint_facts(assets_facts)

```

Note that opening a filing can take **a couple of seconds** depending on the size of the filing.

Once a filing is loaded, it can be queried for its facts, report elements, networks and components.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 18 January 2024

====================

<a id="brel.brel_filing.Filing"></a>

## Filing Objects

```python
class Filing()
```

Represents an XBRL filing in the Open Information Model.

<a id="brel.brel_filing.Filing.open"></a>

#### open

```python
@classmethod
def open(cls, path, *args) -> "Filing"
```

Opens a [`Filing`](#brel.brel_filing.Filing) when given a path. The path can point to one of the following:

- a folder
- a zip file
- an xml file
- multiple xml files

Notes:

- The args parameter is ignored unless the path points to an xml file.
- Depending on the size of the filing, loading can take **a couple of seconds**.

**Arguments**:

- `path`: the path to the filing. This can be a folder, an xml file, or a zip file.
- `args`: additional xml files to load. These are only used if the path is an xml file.

**Raises**:

- `ValueError`: if the path is not a valid path.

**Returns**:

`Filing`: a [`Filing`](#brel.brel_filing.Filing) object with the filing loaded.

<a id="brel.brel_filing.Filing.get_all_facts"></a>

#### get\_all\_facts

```python
def get_all_facts() -> list[Fact]
```

**Returns**:

`list[Fact]`: a list of all [`Fact`](../facts/facts.md) objects in the filing.

<a id="brel.brel_filing.Filing.get_all_report_elements"></a>

#### get\_all\_report\_elements

```python
def get_all_report_elements() -> list[IReportElement]
```

**Returns**:

`list[IReportElement]`: a list of all [`IReportElement`](../report-elements/report-elements.md) objects in the filing.

<a id="brel.brel_filing.Filing.get_all_components"></a>

#### get\_all\_components

```python
def get_all_components() -> list[Component]
```

**Returns**:

`list[Component]`: a list of all [`Component`](../components/components.md) objects in the filing.
Note: components are sometimes called "roles" in the XBRL specification.

<a id="brel.brel_filing.Filing.get_all_physical_networks"></a>

#### get\_all\_physical\_networks

```python
def get_all_physical_networks() -> list[INetwork]
```

Get all [`INetwork`](../components/networks.md) objects in the filing, where network.is_physical() is True.

**Returns**:

`list[INetwork]`: a list of all physical networks in the filing.

<a id="brel.brel_filing.Filing.get_all_concepts"></a>

#### get\_all\_concepts

```python
def get_all_concepts() -> list[Concept]
```

**Returns**:

`list[Concept]`: a list of all concepts in the filing.
Note that concepts are defined according to the Open Information Model. They are not the same as abstracts, line items, hypercubes, dimensions, or members.

<a id="brel.brel_filing.Filing.get_all_abstracts"></a>

#### get\_all\_abstracts

```python
def get_all_abstracts() -> list[Abstract]
```

**Returns**:

`list[Abstract]`: a list of all abstracts in the filing.

<a id="brel.brel_filing.Filing.get_all_line_items"></a>

#### get\_all\_line\_items

```python
def get_all_line_items() -> list[LineItems]
```

**Returns**:

`list[LineItems]`: a list of all line items in the filing.

<a id="brel.brel_filing.Filing.get_all_hypercubes"></a>

#### get\_all\_hypercubes

```python
def get_all_hypercubes() -> list[Hypercube]
```

**Returns**:

`list[Hypercube]`: a list of all hypercubes in the filing.

<a id="brel.brel_filing.Filing.get_all_dimensions"></a>

#### get\_all\_dimensions

```python
def get_all_dimensions() -> list[Dimension]
```

**Returns**:

`list[Dimension]`: a list of all dimensions in the filing.

<a id="brel.brel_filing.Filing.get_all_members"></a>

#### get\_all\_members

```python
def get_all_members() -> list[Member]
```

**Returns**:

`list[Member]`: a list of all members in the filing.

<a id="brel.brel_filing.Filing.get_report_element_by_name"></a>

#### get\_report\_element\_by\_name

```python
def get_report_element_by_name(
        element_qname: QName | str) -> IReportElement | None
```

**Arguments**:

- `element_qname`: the name of the report element to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".

**Raises**:

- `ValueError`: if the QName string is not a valid QName or if the prefix is not found.

**Returns**:

`IReportElement|None`: the report element with the given name. If no report element is found, then None is returned.

<a id="brel.brel_filing.Filing.get_concept_by_name"></a>

#### get\_concept\_by\_name

```python
def get_concept_by_name(concept_qname: QName | str) -> Concept | None
```

**Arguments**:

- `concept_qname`: the name of the concept to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".

**Raises**:

- `ValueError`: if the QName string is not a valid QName or if the prefix is not found.

**Returns**:

`Concept|None`: the concept with the given name. If no concept is found, then None is returned.

<a id="brel.brel_filing.Filing.get_concept"></a>

#### get\_concept

```python
def get_concept(concept_qname: QName | str) -> Concept | None
```

Alias of `filing.get_concept_by_name(concept_qname)`.

<a id="brel.brel_filing.Filing.get_all_reported_concepts"></a>

#### get\_all\_reported\_concepts

```python
def get_all_reported_concepts() -> list[Concept]
```

Returns all concepts that have at least one fact reporting against them.

**Returns**:

`list[Concept]`: The list of concepts

<a id="brel.brel_filing.Filing.get_facts_by_concept_name"></a>

#### get\_facts\_by\_concept\_name

```python
def get_facts_by_concept_name(concept_name: QName | str) -> list[Fact]
```

Returns all facts that are associated with the concept with name concept_name.

**Arguments**:

- `concept_name`: The name of the concept to get facts for. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".

**Raises**:

- `ValueError`: if the QName string but is not a valid QName or if the prefix is not found.

**Returns**:

`list[Fact]`: the list of facts

<a id="brel.brel_filing.Filing.get_facts_by_concept"></a>

#### get\_facts\_by\_concept

```python
def get_facts_by_concept(concept: Concept) -> list[Fact]
```

Returns all facts that are associated with a concept.

**Arguments**:

- `concept`: the concept to get facts for.

**Returns**:

`list[Fact]`: the list of facts

<a id="brel.brel_filing.Filing.get_all_component_uris"></a>

#### get\_all\_component\_uris

```python
def get_all_component_uris() -> list[str]
```

**Returns**:

`list[str]`: a list of all component URIs in the filing.

<a id="brel.brel_filing.Filing.get_component"></a>

#### get\_component

```python
def get_component(uri: str) -> Component | None
```

**Arguments**:

- `URI`: the URI of the component to get.

**Returns**:

`Component|None`: the component with the given URI. None if no component is found.

