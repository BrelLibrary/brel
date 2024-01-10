<a id="brel.characteristics.concept_characteristic"></a>

# brel.characteristics.concept\_characteristic

Contains the class for representing an XBRL concept characteristic

=================

- author: Robin Schmidiger
- version: 0.2
- date: 19 December 2023

=================

<a id="brel.characteristics.concept_characteristic.ConceptCharacteristic"></a>

## ConceptCharacteristic Objects

```python
class ConceptCharacteristic(ICharacteristic)
```

Class for representing a concept characteristic.
The concept characteristic links the `Aspect.CONCEPT` aspect to a concept.

<a id="brel.characteristics.concept_characteristic.ConceptCharacteristic.get_value"></a>

#### get\_value

```python
def get_value() -> Concept
```

**Returns**:

`Concept`: the concept of the characteristic

<a id="brel.characteristics.concept_characteristic.ConceptCharacteristic.get_aspect"></a>

#### get\_aspect

```python
def get_aspect() -> Aspect
```

**Returns**:

`Aspect`: returns the `Aspect.CONCEPT` aspect

