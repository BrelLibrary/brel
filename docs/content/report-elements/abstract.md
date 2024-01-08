<a id="brel.reportelements.abstract"></a>

# brel.reportelements.abstract

This module contains the Abstract class. An abstract a kind of report element that is used to group other report elements.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 30 October 2023

====================

<a id="brel.reportelements.abstract.Abstract"></a>

## Abstract Objects

```python
class Abstract(IReportElement)
```

Class representing an abstract in a BREL report. An abstract is a kind of report element that is used to group other report elements.
They are often used in presentation networks to build a hierarchy of concepts.

The Abstract class implements the IReportElement interface.

<a id="brel.reportelements.abstract.Abstract.get_name"></a>

#### get\_name

```python
def get_name() -> QName
```

Get the name of the abstract element.

**Returns**:

`QName`: containing the name of the abstract element

<a id="brel.reportelements.abstract.Abstract.get_labels"></a>

#### get\_labels

```python
def get_labels() -> list[BrelLabel]
```

Get the labels of the abstract element.

**Returns**:

`list[Label]`: contains the labels of the abstract element

