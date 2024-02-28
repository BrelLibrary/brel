# Brel source code documentation

This folder contains the source code for `Brel`, a Python library for working with financial reports. The library provides a set of tools to load, parse, and analyze financial reports in the XBRL format. The library is designed to be easy to use and to provide a high-level interface for working with financial reports.

XBRL reports are complex and contain a lot of information. This document serves as a quick guide to how `Brel` interprets said standard. 
It is not aimed towards the users of the library, but rather to the developers who want to understand how the library works and how to contribute to it.

If you don't know why XBRL is important, you can find more information about it [here](https://www.xbrl.org/the-standard/what/an-introduction-to-xbrl/).
If you are unfamiliar with XBRL, this page will only give you a high-level overview of the standard. 
For a more in-depth understanding, you should refer to the [XBRL specification](https://specifications.xbrl.org/specifications.html)
or Ghislain Fourny's [XBRL book](https://ghislainfourny.github.io/the-xbrl-book/)

Since XBRL uses a lot of jargon, I have included a glossary of terms at the end of this document.
Additionally, this section is very, very brief. If you want to understand how XBRL works, you can also read 
[my thesis](../docs/thesis_latex/thesis.pdf), 
which has a more in-depth explanation of the standard in its XBRL chapter.

## Quick guide on how XBRL works

### Facts

Glossary terms: [Report](#report) [Fact](#fact), [Context](#context), [Characteristics](#characteristics), [Value](#value)

XBRL is a standard for representing financial reports. It is based on XML and is designed to be machine-readable.
Nowadays, XBRL also supports other formats such as JSON, but the XML format is the most common.

An XBRL report is essentially a collection of facts. Each fact represents a piece of information, such as a monetary value, a date, or a percentage.
For example, a fact could be "The revenue of the Foo company in 2020 was 100,000,000 USD".

Instead of representing this information as a string, XBRL represents a fact as a set of characteristics and a value.
The characteristics of a fact describe what the fact is about and the value is the actual piece of information.
For the example above, XBRL would represent the fact as follows:

- Characteristics:
  - Concept: "Revenue"
  - Period: "2020"
  - Entity: "Foo company"
  - Unit: "USD"
- Value: "100,000,000"

The characteristics of a fact are grouped into a context. A context is a set of characteristics that describe what the fact is about.
For example, the context of the fact above would be "The revenue of the Foo company in 2020".
Brel represents a report using the `Filing` class, a fact using the `Fact` class, and a context using the `Context` class.
All of these classes are defined in the files `brel_filing.py`, `brel_fact.py`, and `brel_context.py`, respectively.

### Characteristics

Glossary terms: [Characteristics](#characteristics), [Aspect](#aspect), [Entity](#entity), [Period](#period), [Unit](#unit), [Concept](#concept), [Explicit Dimension](#explicit-dimension), [Typed Dimension](#typed-dimension)

The characteristics of a context come in different types. The previous section already mentioned some of them: the period, the entity, and the unit.
Two more types of characteristics are explicit dimensions and typed dimensions.

- The period characteristic describes the time period to which the fact refers. It can be a single date, a range of dates, or a duration. It is represented by the `PeriodCharacteristic` class in `Brel`, which is defined in the file `characteristics/period_characteristic.py`.
- The entity characteristic describes the entity to which the fact refers. An entity can be a company, a person, or any other entity. It is represented by the `EntityCharacteristic` class in `Brel`, which is defined in the file `characteristics/entity_characteristic.py`.
- The unit characteristic describes the unit of the fact. It can be a currency, a percentage, or any other unit. It is represented by the `UnitCharacteristic` class in `Brel`, which is defined in the file `characteristics/unit_characteristic.py`.
- The concept characteristic describes what the fact is about. Examples of concepts are "Revenue", "Net income", "Total assets", etc. It is represented by the `ConceptCharacteristic` class in `Brel`, which is defined in the file `characteristics/concept_characteristic.py`.

The concept characteristic is the most important one. It is the characteristic that describes what the fact is about.
It is mandatory for every fact, the other characteristics are optional.

Each characteristic in `Brel` implements the `ICharacteristics` interface, which is defined in the file `characteristics/i_characteristics.py`. Python does not have interfaces, so I use abstract base classes to define the interface.
Each characteristic has to implement two methods: `get_aspect` and `get_value`. The `get_aspect` defines the type of the characteristic (e.g. period, entity, unit, concept, etc.) and the `get_value` returns the value of the characteristic.
For example, for the characteristic "on the 31st of December 2020", `get_aspect` would indicate that it is a period and `get_value` would return the date "2020-12-31".

Aspects are also represented by classes in `Brel`. The `Aspect` class is defined in the file `characteristics/brel_aspect.py`. Each instance of the `Aspect` class represents a different type of characteristic. Therefore, all concepts share the same `Aspect` instance, all periods share the same `Aspect` instance, and so on.

If we only consider the period, entity, and unit characteristics, having a class for each of them might seem like overkill. However, the XBRL standard allows for custom characteristics, which are represented by dimensions. There are two types of dimensions: explicit dimensions and typed dimensions.

- An explicit dimension is a dimension that has a set of predefined values. For example, a company might have a dimension called "Segment" with the values "North America", "Europe", and "Asia". It is represented by the `ExplicitDimensionCharacteristic` class in `Brel`, which is defined in the file `characteristics/explicit_dimension_characteristic.py`.
The `Aspect` of this characteristic will be an instance that represents the "Segment" dimension.
- A typed dimension is a dimension that has a set of values that are not predefined. For example, a company might have a dimension called "Zip code", which can have any integer value. It is represented by the `TypedDimensionCharacteristic` class in `Brel`, which is defined in the file `characteristics/typed_dimension_characteristic.py`.
The `Aspect` of this characteristic will be an instance that represents the "Zip code" dimension.

### Hypercubes

Glossary terms: [Hypercube](#hypercube), [Dimension](#dimension), [Line Items](#line-item)

The XBRL standard allows for facts to be organized into hypercubes. A hypercube is a multi-dimensional structure that groups facts by their characteristics.
In fact, the way facts are represented right now already implies a hypercube: the period, entity, concept, and unit characteristics form a 4-dimensional hypercube.
Additional typed or explicit dimensions add to the number of dimensions of the hypercube.

Since not every fact has every additional dimension, the hypercube is not a perfect grid. Instead, it is sparse, meaning that it has lots of empty cells.

To deal with this sparsity, the XBRL standard allows the whole report hypercube to be sliced into smaller hypercubes. Each hypercube specifies a set of dimensions that it wants to include.

The concept dimension is unique in that a report might define thousands of concepts, but only a few are relevant for a specific hypercube. XBRL introduces the concept of line items. Line items are a subset of the concepts that are relevant for a specific hypercube.

### Networks

Glossary terms: [Network](#network), [Node](#node), [Link](#link), [Arc](#arc), [Report element](#report-element), [Resource](#resource)

So far, reports are merely a collection of facts. However, XBRL reports can represent more complex structures by describing how facts are related to each other.
These structures are called networks in `Brel` and links in the XBRL standard.

A network in `Brel` is a directed graph, where each edge represents a specific kind of relationship between two nodes. 
For example, the concept "Assets" might comprise the concepts "Current assets" and "Non-current assets".
In this case, the network would have a node for the concept "Assets", a node for the concept "Current assets", and a node for the concept "Non-current assets".
Additionally, there would be two `parent-child` edges, one from "Assets" to "Current assets" and one from "Assets" to "Non-current assets".

`Brel` represents networks using the `Network` class, which is defined in the file `networks/i_network.py`. Each network consists of `NetworkNodes` objects defined in `networks/i_network_node.py`.
Each `NetworkNode` can have multiple children, which can in turn have multiple children, and so on. 
The `Network` contains a list of `NetworkNode` objects, which represent the root nodes of the network.
XBRL chooses to call edges "arcs".

Each node in a network represents a report element. The following types of report elements are defined in `Brel`:

- Concept: These link to the concepts of the facts. They are represented by the `Concept` class, which is defined in the file `reportelements/concept.py`.
- Abstract: These are nodes are used to group other nodes. They are represented by the `Abstract` class, which is defined in the file `reportelements/abstract.py`.
- Dimension: These are nodes that represent both explicit and typed dimensions. They are represented by the `Dimension` class, which is defined in the file `reportelements/dimension.py`.
- Member: These are nodes that represent the values of explicit dimensions. They are represented by the `Member` class, which is defined in the file `reportelements/member.py`. Members are the children of dimensions.
- Hypercube: These are nodes that represent the hypercubes of the report. They are represented by the `Hypercube` class, which is defined in the file `reportelements/hypercube.py`. The children of a hypercube in a network are the dimensions of the hypercube.
- Line item: These are nodes that represent the line items of the report. They are represented by the `LineItem` class, which is defined in the file `reportelements/lineitems.py`. The children of a line item in a network are the concepts of the line item.

Besides representing the relationships between report elements, networks also contain resources. Resources are metadata for report elements and facts. They are represented by the `Resource` class, which is defined in the file `resources/resource.py`.
Resources come in 3 flavors: 

- Label: A label is a human-readable name for a report element. It is represented by the `BrelLabel` class, which is defined in the file `resources/brel_label.py`.
- Reference: A reference is a link to a document that provides more information about a report element or a fact. They are similar to citations in a scientific paper. 
They are represented by the `BrelReference` class, which is defined in the file `resources/brel_reference.py`. Unlike labels, references are a dictionary of strings, where the keys are e.g. "Book", "Page", "Paragraph", etc. and the values are the corresponding references.
- Footnote: A footnote is similar to a label, but it can link to report elements and facts. It is represented by the `BrelFootnote` class, which is defined in the file `resources/brel_footnote.py`.

In XBRL and `Brel`, different networks are used to represent relationships. `Brel` uses the following networks:

- Presentation network: This network represents the relationships between report elements in the report.
- Calculation network: This network represents how some concepts are calculated from other concepts.
- Footnote network: This network represents the relationships between report elements and footnotes.
- Label network: This network represents the relationships between report elements and labels.
- Reference network: This network represents the relationships between report elements and references.
- Definition network: This network represents any relationships that are not covered by the other networks.

All of these networks are represented as their own classes in `Brel`. Each class is defined in the `networks` folder.

### Components

Glossary terms: [Component](#component), [Network](#network), [Report](#report), [RoleType](#role-type)

We now know how to represent facts and how to represent the relationships between facts. However, a report is more than just a collection of facts and relationships.
A report is divided into sections, such as the balance sheet, the income statement, and the cash flow statement. Each section contains a set of facts and relationships that are relevant to that section.

In XBRL, these chapters are called RoleTypes and in `Brel` they are called components.
A component in `Brel` is a collection of networks, an ID and an optional label. The networks of a component are limited to presentation, calculation and definition networks.
The `Component` class is defined in the file `brel_component.py`.

Some networks do not belong to any component and are report-wide. These are the footnote, label, and reference networks. 

### Parsing

Glossary terms: [Parser](#parser), [XBRL](#xbrl), [XML](#xml), [JSON](#json)

So far, we have only talked about how `Brel` represents XBRL reports. However, the library also contains code to parse XBRL reports from their raw format into the `Brel` format.
The parsing code is located in the `parsers` folder.
Currently, `Brel` supports parsing XBRL reports in XML format. 
Intuitively, each class in `Brel` has a corresponding file in the `parsers` with a few exceptions.
Brel employs a bottom-up approach to parsing, meaning that it parses XBRL in the following order: report elements -> facts -> networks -> components -> report.
Documentation for the parsers are located in the respective files.

### Glossary

#### Report

A report is a collection of facts, components, and networks. It is the highest-level object in `Brel`.

#### Fact

A fact is a piece of information in an XBRL report. It is represented by the `Fact` class in `Brel`.

#### Context

A context is a set of characteristics that describe what a fact is about. It is represented by the `Context` class in `Brel`.

#### Characteristics

Characteristics are the attributes of a fact. They describe what the fact is about. They are represented by the `ICharacteristics` interface in `Brel`.

#### Value

The value of a fact. It is the actual piece of information that the fact represents.

#### Aspect

An aspect is a type of characteristic. It is represented by the `Aspect` class in `Brel`.

#### Entity

The entity characteristic describes the entity to which the fact refers. It is represented by the `EntityCharacteristic` class in `Brel`.

#### Period

The period characteristic describes the time period to which the fact refers. It is represented by the `PeriodCharacteristic` class in `Brel`.

#### Unit

The unit characteristic describes the unit of the fact. It is represented by the `UnitCharacteristic` class in `Brel`.

#### Concept

The concept characteristic describes what the fact is about. It is represented by the `ConceptCharacteristic` class in `Brel`.

#### Explicit Dimension

The explicit dimension characteristic describes a dimension that has a set of predefined values. It is represented by the `ExplicitDimensionCharacteristic` class in `Brel`.

#### Typed Dimension

The typed dimension characteristic describes a dimension that has a set of values that are not predefined. It is represented by the `TypedDimensionCharacteristic` class in `Brel`.

#### Hypercube

A hypercube is a multi-dimensional structure that groups facts by their characteristics.
Each cell in the hypercube represents a fact. It is represented by the `Hypercube` class in `Brel`.

#### Dimension

Dimensions are the characteristics of a hypercube. They are represented by the different classes that implement the `ICharacteristics` interface in `Brel`.

#### Line Item

Line items are a subset of the concepts that are relevant for a specific hypercube. They are represented by the `LineItem` class in `Brel`.

#### Network

A network is a directed graph that represents the relationships between report elements, facts, and resources. It is represented by the `INetwork` interface in `Brel`.

#### Node

A node is an element of a network. It is represented by the `INetworkNode` interface in `Brel`.
They can have other nodes as children.
Each node can point to either a report element, a resource, or a fact.

#### Link

A link is the XBRL term for a network. 

#### Arc

An arc is the XBRL term for an edge in a network.

#### Report Element

A report element is a building of a building block of a report. It is represented by the different classes in the `reportelements` folder in `Brel`.
Report elements make up the nodes of a network.
Some report elements like concepts, dimensions and members are also used to define the characteristics of facts.

#### Resource

A resource is metadata for report elements and facts. It is represented by the `IResource` interface in `Brel`.

#### Component

A component is a collection of networks, an ID and an optional label. It is represented by the `Component` class in `Brel`.
It represents a chapter in an XBRL report.

#### RoleType

A RoleType is the XBRL term for a component.

#### Parser

A parser is a class that turns raw XBRL data into the python objects used in `Brel`. It is represented by the different files in the `parsers` folder in `Brel`.

#### XBRL

XBRL is a standard for representing financial reports. It is based on XML and is designed to be machine-readable.

#### XML

XML is a markup language that is used to represent structured data. It is the most common format for XBRL reports.
`Brel` supports parsing XBRL reports in XML format.

#### JSON

JSON is a format for representing structured data. It is an alternative to XML for representing XBRL reports.
`Brel` does not support parsing XBRL reports in JSON format.

## How to contribute

If you want to contribute to `Brel`, you can start by reading the source code in this folder.
The source code is well-documented and should give you a good understanding of how the library works.

You can also contribute by writing tests for the library. The tests are located in the `tests` folder.

If you want to contribute to the documentation, you can do so by writing documentation for the library. The documentation is located in the `docs` folder.
Additionally, `Brel` automatically generates documentation from the source code using `pydoc-markdown` and `mkdocs`. 
Install them using:

```bash
pip install -r requirements-test.txt
```

You can edit how the documentation is generated by editing the `pydoc-markdown.yml` file in the project root. You can rebuild the documentation by running `make docs` and you can deploy the documentation by running `make docs-deploy`.

**Build and view locally**

```bash
make docs
mkdocs serve
```

Then click on the link that appears in the terminal.

**Deploy to GitHub pages**

```bash
make docs-deploy
```

If you want to contribute to the library, you can do so by writing code for the library. The source code is located in the `brel` folder.
