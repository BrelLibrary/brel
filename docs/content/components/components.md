<a id="brel.brel_component"></a>

# brel.brel\_component

This module contains the Component class.
Components are used to define the presentation, calculation and definition networks of a filing.

Intuitively, they function as the chapters of a report or filing. Note that XBRL sometimes calls components 'roles'.

Given a report, you can get all the components using the `Filing.get_all_components()` method.

If you are looking for a specific component, consider the following:

```python
all_component_URIs = filing.get_all_component_URIs()

# select one of the component names from the list
my_component_name = all_component_URIs[0]

# get the component
my_component = filing.get_component(my_component_name)
```

Components act as wrappers for the [`Network`s](#.networks/index.md) of a filing. 
The most notable kind of networks are the presentation, calculation and definition networks.

- get the [`PresentationNetwork`](#./networks/presentation_network.md) using the `Component.get_presentation_network()` method.
- get the [`CalculationNetwork`](#./networks/calculation_network.md) using the `Component.get_calculation_network()` method.
- get the [`DefinitionNetwork`](#./networks/definition_network.md) using the `Component.get_definition_network()` method.

You can print them using the `pprint_network` function in the `brel` module:

```python
from brel import pprint

calculation_network = my_component.get_calculation_network()
pprint(calculation_network)
```

====================

- author: Robin Schmidiger
- version: 0.6
- date: 07 January 2024

====================

<a id="brel.brel_component.Component"></a>

## Component Objects

```python
class Component()
```

This class implements XBRL components, which are sometimes also called roles.
Components are used to define the presentation, calculation and definition networks of a filing.
Intuitively, they function as the chapters of a report or filing.

A component consists of the following:

- a URI, also called the roleURI. This is the identifier of the component.
- an info, also called the definition. This is a string that describes the component. It is optional.
- a set of networks. The most notable kind of networks are the presentation, calculation and definition networks.

<a id="brel.brel_component.Component.get_URI"></a>

#### get\_URI

```python
def get_URI() -> str
```

**Returns**:

`str`: the URI of the component

<a id="brel.brel_component.Component.get_info"></a>

#### get\_info

```python
def get_info() -> str
```

**Returns**:

`str`: the info/definition of the component.

<a id="brel.brel_component.Component.get_presentation_network"></a>

#### get\_presentation\_network

```python
def get_presentation_network() -> PresentationNetwork | None
```

**Returns**:

`PresentationNetwork`: the presentation network of the component. None if the component has no presentation network or if the network is empty.

<a id="brel.brel_component.Component.get_calculation_network"></a>

#### get\_calculation\_network

```python
def get_calculation_network() -> CalculationNetwork | None
```

**Returns**:

`CalculationNetwork`: the calculation network of the component. None if the component has no calculation network or if the network is empty.

<a id="brel.brel_component.Component.get_definition_network"></a>

#### get\_definition\_network

```python
def get_definition_network() -> DefinitionNetwork | None
```

**Returns**:

`DefinitionNetwork`: the definition network of the component. None if the component has no definition network or if the network is empty.

<a id="brel.brel_component.Component.has_presentation_network"></a>

#### has\_presentation\_network

```python
def has_presentation_network() -> bool
```

**Returns**:

`bool`: True if the component has a presentation network, False otherwise

<a id="brel.brel_component.Component.has_calculation_network"></a>

#### has\_calculation\_network

```python
def has_calculation_network() -> bool
```

**Returns**:

`bool`: True if the component has a calculation network, False otherwise

<a id="brel.brel_component.Component.has_definition_network"></a>

#### has\_definition\_network

```python
def has_definition_network() -> bool
```

**Returns**:

`bool`: True if the component has a definition network, False otherwise

<a id="brel.brel_component.Component.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

**Returns**:

`str`: a string representation of the component

<a id="brel.brel_component.Component.is_aggregation_consistent"></a>

#### is\_aggregation\_consistent

```python
def is_aggregation_consistent(facts: list[Fact]) -> bool
```

**Arguments**:

- `facts`: the facts of the filing

**Returns**:

`bool`: True if and only if the component is aggregation consistent against the given facts

