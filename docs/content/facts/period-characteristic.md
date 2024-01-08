<a id="brel.characteristics.period_characteristic"></a>

# brel.characteristics.period\_characteristic

This module contains the PeriodCharacteristic class, which represents an XBRL period characteristic.
A period characteristic associates the aspect Aspect.PERIOD with a value.
This value can be an instant or a duration.

An instant consists of a single `datetime.date` instance.

A duration consists of two `datetime.date` instances, a start date and an end date.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 08 Jan 2024

====================

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic"></a>

## PeriodCharacteristic Objects

```python
class PeriodCharacteristic(ICharacteristic)
```

Class for representing an XBRL period characteristic.
A period characteristic is either a duration or an instant.
Use the `is_instant()` method to check if the period is an instant or a duration.

If the period is an instant, use the `get_instant_period()` method to get the instant date as a `datetime.date` instance.

if the period is a duration, use the `get_start_period()` and `get_end_period()` methods to get the start and end dates as `datetime.date` instances.

A quirk of the `PeriodCharacteristic.get_value()` method is that it returns the period characteristic itself.

This is because the standard python package `datetime` does not have a class for representing a period as specified by XBRL.

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.is_instant"></a>

#### is\_instant

```python
def is_instant() -> bool
```

**Returns**:

`bool`: True if the period is an instant, False otherwise

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.get_start_period"></a>

#### get\_start\_period

```python
def get_start_period() -> datetime.date
```

**Raises**:

- `ValueError`: if the period is an instant. Use 'is_instant' to check if the period is an instant.

**Returns**:

`datetime.date`: the start date of the period as a `datetime.date` instance.

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.get_end_period"></a>

#### get\_end\_period

```python
def get_end_period() -> datetime.date
```

**Raises**:

- `ValueError`: if the period is an instant. Use 'is_instant' to check if the period is an instant.

**Returns**:

`datetime.date`: the end date of the period as a `datetime.date` instance.

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.get_instant_period"></a>

#### get\_instant\_period

```python
def get_instant_period() -> datetime.date
```

**Raises**:

- `ValueError`: if the period is a duration. Use 'is_instant' to check if the period is an instant.

**Returns**:

`datetime.date`: the instant date of the period as a `datetime.date` instance.

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> "PeriodCharacteristic"
```

**Returns**:

`PeriodCharacteristic`: the period characteristic itself

<a id="brel.characteristics.period_characteristic.PeriodCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

**Returns**:

`Aspect`: the aspect of the period characteristic, which is `Aspect.PERIOD`

