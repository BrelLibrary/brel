<a id="brel.reportelements.i_report_element"></a>

# brel.reportelements.i\_report\_element

This module contains the interface for all report elements.
Report elements are the building blocks of a report and are used by a lot of other classes.
Therefore, it is important to have a common interface for all report elements.

Report have a unique name and can have multiple human readable labels representing the same name.
Depending on the kind of report element, there might be more information available.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 21 January 2024

====================

<a id="brel.reportelements.i_report_element.IReportElement"></a>

## IReportElement Objects

```python
class IReportElement(ABC)
```

Interface for all report elements.
Each report element must have a name and can have multiple labels.

<a id="brel.reportelements.i_report_element.IReportElement.get_name"></a>

#### get\_name

```python
@abstractmethod
def get_name() -> QName
```

Get the name of the report element.

**Returns**:

QName containing the name of the report element

<a id="brel.reportelements.i_report_element.IReportElement.get_labels"></a>

#### get\_labels

```python
@abstractmethod
def get_labels() -> list[BrelLabel]
```

Get all labels of the report element.

**Returns**:

`list[Label]`: containing the labels of the report element

<a id="brel.reportelements.i_report_element.IReportElement.has_label_with_role"></a>

#### has\_label\_with\_role

```python
def has_label_with_role(label_role: str) -> bool
```

Check if the report element has a label with the given role.

**Arguments**:

- `label_role`: the role of the label to check

**Returns**:

`bool`: True if the report element has a label with the given role, False otherwise

<a id="brel.reportelements.i_report_element.IReportElement.has_label_with_language"></a>

#### has\_label\_with\_language

```python
def has_label_with_language(language: str) -> bool
```

Check if the report element has a label with the given language.

**Arguments**:

- `language`: the language of the label to check

**Returns**:

`bool`: True if the report element has a label with the given language, False otherwise

