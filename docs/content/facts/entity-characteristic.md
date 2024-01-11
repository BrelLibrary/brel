<a id="brel.characteristics.entity_characteristic"></a>

# brel.characteristics.entity\_characteristic

Contains the class for representing an XBRL entity.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 07 January 2024

====================

<a id="brel.characteristics.entity_characteristic.EntityCharacteristic"></a>

## EntityCharacteristic Objects

```python
class EntityCharacteristic(ICharacteristic)
```

Class for representing an XBRL entity.
An entity in XBRL is a company. It consists of an identifier. Usually the identifier is the company's CIK.
Additional information about the company can be found in the entity's segment.

<a id="brel.characteristics.entity_characteristic.EntityCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

**Returns**:

`Aspect`: returns `Aspect.ENTITY`

<a id="brel.characteristics.entity_characteristic.EntityCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> str
```

returns the value of the entity characteristic,

which is the entity's qname in clark notation

- The url of of the QName is the scheme of the entity characteristic.
- The local name of the QName is the id of the entity characteristic.

Example of an entity characteristic value: {http:www.sec.gov/CIK}0000123456

**Returns**:

`str`: the entity's QName in clark notation

<a id="brel.characteristics.entity_characteristic.EntityCharacteristic.get_schema"></a>

#### get\_schema

```python
def get_schema() -> str
```

**Returns**:

`str`: the schema of the entity.

