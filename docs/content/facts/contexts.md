<a id="brel.brel_context"></a>

# brel.brel\_context

This module contains the Context class.

Contexts are what puts facts into context.
For example, take the following fact:

- The Foo Corporation had a Total Revenue of 1'000'000 USD in 2020.

The context of this fact would be:

- Entity: Foo Corporation
- Period: 2020
- Concept: Total Revenue
- Unit: USD

Note that the value 1000000 is not part of the context. It is the value of the fact.

Contexts consist of aspects and their associated characteristics.
In the example above, the aspects are Entity, Period, Concept and Unit.
Characteristics are aspect-value pairs.
So for example, the characteristic of the Entity aspect would be "Foo Corporation".

Read more about Aspects and Characteristics in 

====================

- author: Robin Schmidiger
- version: 0.12
- date: 07 January 2024

====================

<a id="brel.brel_context.Context"></a>

## Context Objects

```python
class Context()
```

Class for representing an XBRL context.
an XBRL context is a collection of aspects and characteristics.
There are different types of aspects: concept, period, entity, unit and dimensions
The only required aspect is the concept.
All aspects can only be present once.
Dimensions are custom aspects, so they can be present multiple times as long as they represent different dimensions.

<a id="brel.brel_context.Context.get_aspects"></a>

#### get\_aspects

```python
def get_aspects() -> list[Aspect]
```

Get all aspects of the context.

**Returns**:

`list[Aspect]`: The aspects of the context.

<a id="brel.brel_context.Context.get_characteristic"></a>

#### get\_characteristic

```python
def get_characteristic(aspect: Aspect) -> ICharacteristic | None
```

Get the value of an aspect.

**Arguments**:

- `aspect`: The aspect to get the value of.

**Returns**:

`Aspect|None`: The value of the aspect. None if the aspect is not present in the context.

<a id="brel.brel_context.Context.has_characteristic"></a>

#### has\_characteristic

```python
def has_characteristic(aspect: Aspect) -> bool
```

Check if the context has a certain aspect.

**Arguments**:

- `aspect`: The aspect to check for.

**Returns**:

`bool`: True if the context has the aspect, False otherwise.

<a id="brel.brel_context.Context.get_characteristic_as_str"></a>

#### get\_characteristic\_as\_str

```python
def get_characteristic_as_str(aspect: Aspect) -> str
```

Get the value of an aspect as a string.

This is a convenience function.
The representation of aspects as strings is not standardized.
If the aspect is not present in the context, an empty string is returned.

**Arguments**:

- `aspect`: The aspect to get the value of.

**Returns**:

`str`: The value of the aspect as a string.

<a id="brel.brel_context.Context.get_characteristic_as_int"></a>

#### get\_characteristic\_as\_int

```python
def get_characteristic_as_int(aspect: Aspect) -> int
```

Get the value of an aspect as an int.

This is a convenience function.
If the aspect is not present in the context, 0 is returned.

**Arguments**:

- `aspect`: The aspect to get the value of.

**Raises**:

- `ValueError`: If the aspect is present, but the value cannot be converted to an int.

**Returns**:

`int`: The value of the aspect as an int.

<a id="brel.brel_context.Context.get_characteristic_as_float"></a>

#### get\_characteristic\_as\_float

```python
def get_characteristic_as_float(aspect: Aspect) -> float
```

Get the value of an aspect as a float.

This is a convenience function.
If the aspect is not present in the context, 0.0 is returned.

**Arguments**:

- `aspect`: The aspect to get the value of.

**Raises**:

- `ValueError`: If the aspect is present, but the value cannot be converted to a float.

**Returns**:

`float`: The value of the aspect as a float.

<a id="brel.brel_context.Context.get_characteristic_as_bool"></a>

#### get\_characteristic\_as\_bool

```python
def get_characteristic_as_bool(aspect: Aspect) -> bool
```

Get the value of an aspect as a bool.

This is a convenience function.
If the aspect is not present in the context, False is returned.

**Arguments**:

- `aspect`: The aspect to get the value of.

**Raises**:

- `ValueError`: If the aspect is present, but the value cannot be converted to a bool.

**Returns**:

`bool`: The value of the aspect as a bool.

<a id="brel.brel_context.Context.get_concept"></a>

#### get\_concept

```python
def get_concept() -> ConceptCharacteristic
```

Get the concept of the context.

This function is equivalent to `get_characteristic(Aspect.CONCEPT)`.
It cannot return None, because the concept is a required aspect.

**Returns**:

`ConceptCharacteristic`: The concept of the context.

<a id="brel.brel_context.Context.get_period"></a>

#### get\_period

```python
def get_period() -> PeriodCharacteristic | None
```

Get the period of the context.

This function is equivalent to `get_characteristic(Aspect.PERIOD)`.

**Returns**:

`PeriodCharacteristic|None`: The period of the context. None if the context does not have a period.

<a id="brel.brel_context.Context.get_entity"></a>

#### get\_entity

```python
def get_entity() -> EntityCharacteristic | None
```

Get the entity of the context.

This function is equivalent to `get_characteristic(Aspect.ENTITY)`.

**Returns**:

`EntityCharacteristic|None`: The entity of the context. None if the context does not have an entity.

<a id="brel.brel_context.Context.get_unit"></a>

#### get\_unit

```python
def get_unit() -> UnitCharacteristic | None
```

Get the unit of the context.

This function is equivalent to `get_characteristic(Aspect.UNIT)`.

**Returns**:

`UnitCharacteristic|None`: The unit of the context. None if the context does not have a unit.

