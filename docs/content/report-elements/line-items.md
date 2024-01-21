<a id="brel.reportelements.lineitems"></a>

# brel.reportelements.lineitems

This module contains the LineItems class.

=================

- author: Robin Schmidiger
- version: 0.2
- date: 18 January 2024

=================

<a id="brel.reportelements.lineitems.LineItems"></a>

## LineItems Objects

```python
class LineItems(IReportElement)
```

<a id="brel.reportelements.lineitems.LineItems.get_name"></a>

#### get\_name

```python
def get_name() -> QName
```

**Returns**:

`QName`: the name of the line items as a QName

<a id="brel.reportelements.lineitems.LineItems.get_labels"></a>

#### get\_labels

```python
def get_labels() -> list[BrelLabel]
```

**Returns**:

`list[BrelLabel]`: the labels of the line items

<a id="brel.reportelements.lineitems.LineItems.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

**Returns**:

`str`: the name of the line items as a string

