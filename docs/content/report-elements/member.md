<a id="brel.reportelements.member"></a>

# brel.reportelements.member

This module contains the class for the Member report element in Brel.
Members are used to represent the possible values of an explicit dimension.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 18 January 2023

====================

<a id="brel.reportelements.member.Member"></a>

## Member Objects

```python
class Member(IReportElement)
```

Class representing a member in a BREL report. A member is a kind of report element that is used to represent the possible values of an explicit dimension.
It implements the IReportElement interface.

<a id="brel.reportelements.member.Member.get_name"></a>

#### get\_name

```python
def get_name() -> QName
```

**Returns**:

`QName`: the name of the member as a QName

<a id="brel.reportelements.member.Member.get_labels"></a>

#### get\_labels

```python
def get_labels() -> list[BrelLabel]
```

**Returns**:

`list[BrelLabel]`: the labels of the member

