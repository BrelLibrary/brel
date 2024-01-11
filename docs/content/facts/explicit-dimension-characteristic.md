<a id="brel.characteristics.explicit_dimension_characteristic"></a>

# brel.characteristics.explicit\_dimension\_characteristic

This module contains the class for representing an explicit dimension characteristic.
Explicit members are a wrapper for a dimension- and a member report element.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 2023-12-06

====================

<a id="brel.characteristics.explicit_dimension_characteristic.ExplicitDimensionCharacteristic"></a>

## ExplicitDimensionCharacteristic Objects

```python
class ExplicitDimensionCharacteristic(ICharacteristic)
```

Class for representing an explicit dimension characteristic.
An explicit dimension characteristic assigns a dimension a member.

The dimension is both a dimension report element as well as an aspect with the same QName as
the dimension report element.

The member is a member report element and the value of the explicit dimension characteristic.

<a id="brel.characteristics.explicit_dimension_characteristic.ExplicitDimensionCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

Info: Both typed and explicit dimension characteristics are not statically bound to an

aspect.

**Returns**:

`Aspect`: the aspect of the explicit dimension characteristic.

<a id="brel.characteristics.explicit_dimension_characteristic.ExplicitDimensionCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> Member
```

returns the value of the explicit dimension characteristic.

Values of explicit dimension characteristics are member report elements.

**Returns**:

`Member`: the member of the explicit dimension characteristic.

<a id="brel.characteristics.explicit_dimension_characteristic.ExplicitDimensionCharacteristic.get_dimension"></a>

#### get\_dimension

```python
def get_dimension() -> Dimension
```

returns the name/dimension/axis of the explicit dimension characteristic.

Names of explicit dimension characteristics are dimensions.
This is not the same as calling `get_aspect()`.

**Returns**:

`Dimension`: the dimension of the explicit dimension characteristic.

<a id="brel.characteristics.explicit_dimension_characteristic.ExplicitDimensionCharacteristic.get_member"></a>

#### get\_member

```python
def get_member() -> Member
```

returns the member of the explicit dimension characteristic.

This is equivalent to calling `get_value()`.

**Returns**:

`Member`: the member of the explicit dimension characteristic.

