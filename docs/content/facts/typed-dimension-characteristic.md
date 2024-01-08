<a id="brel.characteristics.typed_dimension_characteristic"></a>

# brel.characteristics.typed\_dimension\_characteristic

This module contains the class for  the typed dimension characteristic in Brel.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 19 December 2023

====================

<a id="brel.characteristics.typed_dimension_characteristic.TypedDimensionCharacteristic"></a>

## TypedDimensionCharacteristic Objects

```python
class TypedDimensionCharacteristic(ICharacteristic)
```

Class for representing a typed dimension characteristic.
A typed dimension characteristic assigns a dimension aspect a value.
In Brel, the type of the value is omitted and the value is always a string.

<a id="brel.characteristics.typed_dimension_characteristic.TypedDimensionCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

Info: Both typed and explicit dimension characteristics are not core characteristics and therefore not available as attributes of the `Aspect` class.

**Returns**:

`Aspect`: the aspect of the explicit dimension characteristic.

<a id="brel.characteristics.typed_dimension_characteristic.TypedDimensionCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> str
```

**Returns**:

`str`: the value of the typed dimension characteristic as a string.

<a id="brel.characteristics.typed_dimension_characteristic.TypedDimensionCharacteristic.get_dimension"></a>

#### get\_dimension

```python
def get_dimension() -> Dimension
```

Info: this is not the same as calling `get_aspect()`.

**Returns**:

`Dimension`: the dimension of the typed dimension characteristic.

