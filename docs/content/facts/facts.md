<a id="brel.brel_fact"></a>

# brel.brel\_fact

This module contains the Fact class.

Facts in Brel are the atomic pieces of information. They consist of a value, a context and an id.
They closely resemble the facts in XBRL in the Open Information Model.

To print a fact to the console, use the `pprint_fact` function in the `brel` module.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 06 January 2024

====================

<a id="brel.brel_fact.Fact"></a>

## Fact Objects

```python
class Fact()
```

The Fact class consists of a value, a context and an id.

- The value is the value of the fact. It is a string.
- The context is the context of the fact. It is a Context object.
- The id is the id of the fact. It is a string and is optional.

<a id="brel.brel_fact.Fact.get_context"></a>

#### get\_context

```python
def get_context() -> Context
```

**Returns**:

`Context`: The context of the fact as a Context object.

<a id="brel.brel_fact.Fact.get_value_as_str"></a>

#### get\_value\_as\_str

```python
def get_value_as_str() -> str
```

**Returns**:

`str`: The value of the fact as a string.

<a id="brel.brel_fact.Fact.get_value_as_qname"></a>

#### get\_value\_as\_qname

```python
def get_value_as_qname() -> QName
```

**Returns**:

The value of the fact as a QName

<a id="brel.brel_fact.Fact.get_value_as_int"></a>

#### get\_value\_as\_int

```python
def get_value_as_int() -> int
```

**Raises**:

- `ValueError`: If the value of the fact does not resolve to an int

**Returns**:

`int`: The value of the fact as an int

<a id="brel.brel_fact.Fact.get_value_as_float"></a>

#### get\_value\_as\_float

```python
def get_value_as_float() -> float
```

**Raises**:

- `ValueError`: If the value of the fact does not resolve to a float

**Returns**:

`float`: The value of the fact as a float

<a id="brel.brel_fact.Fact.get_value_as_bool"></a>

#### get\_value\_as\_bool

```python
def get_value_as_bool() -> bool
```

**Raises**:

- `ValueError`: If the value of the fact does not resolve to a bool

**Returns**:

`bool`: The value of the fact as a bool

<a id="brel.brel_fact.Fact.get_value"></a>

#### get\_value

```python
def get_value() -> Any
```

**Returns**:

`Any`: The value of the fact. The type of the value depends on the type of the fact.

<a id="brel.brel_fact.Fact.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

**Returns**:

`str`: The fact represented as a string.

<a id="brel.brel_fact.Fact.get_concept"></a>

#### get\_concept

```python
def get_concept() -> ConceptCharacteristic
```

**Returns**:

`ConceptCharacteristic`: The concept characteristic of the facts context.
Equivalent to calling `fact.get_context().get_concept()`

<a id="brel.brel_fact.Fact.get_unit"></a>

#### get\_unit

```python
def get_unit() -> UnitCharacteristic | None
```

**Returns**:

`UnitCharacteristic|None`: The unit characteristic of the facts context. Returns None if the fact does not have a unit.
Equivalent to calling `fact.get_context().get_unit()`

<a id="brel.brel_fact.Fact.get_period"></a>

#### get\_period

```python
def get_period() -> PeriodCharacteristic | None
```

**Returns**:

`PeriodCharacteristic|None`: The period characteristic of the facts context. Returns None if the fact does not have a period.
Equivalent to calling `fact.get_context().get_period()`

<a id="brel.brel_fact.Fact.get_aspects"></a>

#### get\_aspects

```python
def get_aspects() -> list[Aspect]
```

**Returns**:

`list[BrelAspect]`: The aspects of the facts context.
Equivalent to calling `fact.get_context().get_aspects()`

<a id="brel.brel_fact.Fact.get_characteristic"></a>

#### get\_characteristic

```python
def get_characteristic(aspect: Aspect) -> ICharacteristic | None
```

Given an aspect, get the associated characteristic of the fact.

**Arguments**:

- `aspect`: The aspect for which the characteristic should be returned.

**Returns**:

`ICharacteristic|None`: The characteristic associated with the given aspect. Returns None if the fact does not have the given aspect.
Equivalent to calling `fact.get_context().get_characteristic(aspect)`

