<a id="brel.reportelements.concept"></a>

# brel.reportelements.concept

This module contains the Concept class. A Concept is a data item that can be reported on.
Concepts in BREL reports are the same as concepts in XBRL reports.
For more information on concepts, see the [**XBRL 2.1 specification**](https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html)

====================

- author: Robin Schmidiger
- version: 0.5
- date: 04 December 2023

====================

<a id="brel.reportelements.concept.Concept"></a>

## Concept Objects

```python
class Concept(IReportElement)
```

Class representing a concept in a BREL report. A concept is a data item that can be reported on.
Concepts in BREL reports are the same as concepts in XBRL reports.
For more information on concepts, see the XBRL 2.1 specification.
A short summary of the most important attributes of a concept:

- It is defined in the XBRL taxonomy. So in the .xsd files in the DTS.
- It has a name, which is a QName. This has to be unique in the DTS.
- It has a data type, which is a QName.
- It has a period type, which can be either instant or duration.
- (optional) It has a balance type, which can be either credit or debit.
- (optional) It can be nillable, which is either true or false. If the attribute is not present, it defaults to false.

<a id="brel.reportelements.concept.Concept.get_name"></a>

#### get\_name

```python
def get_name() -> QName
```

Get the name of the concept.

**Returns**:

`QName`: the QName of the concept

<a id="brel.reportelements.concept.Concept.get_labels"></a>

#### get\_labels

```python
def get_labels() -> list[BrelLabel]
```

Get the labels of the concept.

**Returns**:

`list[Label]`: all labels of the concept

<a id="brel.reportelements.concept.Concept.get_period_type"></a>

#### get\_period\_type

```python
def get_period_type() -> str
```

Get the period type of the concept.

**Returns**:

`str`: the period type of the concept

<a id="brel.reportelements.concept.Concept.get_data_type"></a>

#### get\_data\_type

```python
def get_data_type() -> str
```

Get the data type of the concept.

**Returns**:

`str`: the data type of the concept

<a id="brel.reportelements.concept.Concept.get_balance_type"></a>

#### get\_balance\_type

```python
def get_balance_type() -> str | None
```

Get the balance type of the concept.

**Returns**:

`str|None`: the balance type of the concept. None if the concept has no balance type.

<a id="brel.reportelements.concept.Concept.is_nillable"></a>

#### is\_nillable

```python
def is_nillable() -> bool
```

Check if the concept is nillable.

**Returns**:

`bool`: True 'IFF' the concept is nillable, False otherwise

