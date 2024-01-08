<a id="brel.characteristics.unit_characteristic"></a>

# brel.characteristics.unit\_characteristic

This module contains the class for representing xbrl unit characteristics.
A unit characteristic associates the aspect Aspect.UNIT with a value.
In case of the UnitCharacteristic class, the value is a string.

However, the UnitCharacteristic can also handle more complex units consisting of numerators and denominators.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 07 January 2024

====================

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic"></a>

## UnitCharacteristic Objects

```python
class UnitCharacteristic(ICharacteristic)
```

Class for representing an XBRL unit characteristic.
A unit characteristic associates the aspect Aspect.UNIT with a value and implements the ICharacteristic interface.

A unit can be identified by its name, which usually indicates how the unit is composed.

Examples: "usd", "sharesPerUSD", "shares"

A unit consists of numerators and denominators, which are lists of QNames.

Most units are simple and consist of a single QName.
You can use the `is_simple()` method to check if the unit is simple.

You can get the numerators and denominators of the unit using the `get_numerators()` and `get_denominators()` methods respectively.

The unit characteristic does have a connection to the concept characteristic.
Namely, if the concept characteristic's concept is a monetary concept, the unit's numerators and denominators must be defined in the iso4217 namespace.

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

**Returns**:

`Aspect`: returns Aspect.UNIT

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic.get_numerators"></a>

#### get\_numerators

```python
def get_numerators() -> list[QName]
```

**Returns**:

`list[QName]`: all numerators of the unit

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic.get_denominators"></a>

#### get\_denominators

```python
def get_denominators() -> list[QName]
```

**Returns**:

`list[QName]`: all denominators of the unit

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> str
```

info: this is different from the numerators/denominators of the unit. It is the name of the unit.

**Returns**:

`str`: the name of the unit

<a id="brel.characteristics.unit_characteristic.UnitCharacteristic.is_simple"></a>

#### is\_simple

```python
def is_simple() -> bool
```

A unit is simple if it has exactly one numerator and no denominators

**Returns**:

`bool`: True 'IFF' the unit is simple, False otherwise

