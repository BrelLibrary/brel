<a id="brel.reportelements.dimension"></a>

# brel.reportelements.dimension

This module contains the Dimension class. A dimension is a kind of report element that is used to present additional aspects for the context of a fact.

Facts in Brel can already be viewed as a form of hypercube. Dimensions build on top of that and allow for custom dimensions to be added to the hypercube besides the already existing ones.
The already existing dimensions are the core aspects of a fact, namely the period, the entity, the unit and the concept.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 30 October 2023

====================

<a id="brel.reportelements.dimension.Dimension"></a>

## Dimension Objects

```python
class Dimension(IReportElement)
```

Class representing a dimension in a BREL report. A dimension is a kind of report element that is used to present additional aspects for the context of a fact.

All dimensions are either explicit or typed.
A new dimension is explicit by default.
If you want to make a dimension typed, you have to call `make_typed(dim_type: QName)` on it.

<a id="brel.reportelements.dimension.Dimension.get_name"></a>

#### get\_name

```python
def get_name() -> QName
```

Get the name of the dimension.

**Returns**:

`QName`: the name of the dimension as a QName

<a id="brel.reportelements.dimension.Dimension.get_labels"></a>

#### get\_labels

```python
def get_labels() -> list[BrelLabel]
```

Get the labels of the dimension.

**Returns**:

`list[Label]`: all labels of the dimension

<a id="brel.reportelements.dimension.Dimension.is_explicit"></a>

#### is\_explicit

```python
def is_explicit() -> bool
```

Check if the dimension is explicit.

Use the `make_typed(dim_type: QName)` method to make a dimension typed.

**Returns**:

`bool`: True 'IFF' the dimension is explicit, False otherwise

<a id="brel.reportelements.dimension.Dimension.get_type"></a>

#### get\_type

```python
def get_type() -> QName
```

Get the type of the dimension.

**Raises**:

- `ValueError`: if the dimension is explicit and has no type
Use `is_explicit()` to check if the dimension is explicit.

**Returns**:

`QName`: type of the dimension

<a id="brel.reportelements.dimension.Dimension.make_typed"></a>

#### make\_typed

```python
def make_typed(dim_type: QName)
```

Turn the dimension into a typed dimension.

**Arguments**:

- `dim_type`: the type of the dimension. Has to be a QName

