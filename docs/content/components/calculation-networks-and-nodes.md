<a id="brel.networks.calculation_network_node"></a>

# brel.networks.calculation\_network\_node

This module contains the CalculationNetworkNode class.
CalculationNetworkNodes are used to represent nodes in a calculation network.
Since a node can have children, nodes can also be viewed as trees.
Note: the balance consistency check is not implemented here, but in the CalculationNetwork class.
CalculationNetworkNodes implement the INetworkNode interface, but they add the methods `get_concept()` and `get_weight()`.

Note that this documentation omits the methods inherited from the INetworkNode interface.
For more on the methods inherited from the INetworkNode interface, see the [INetworkNode documentation](./network-nodes.md).

=================

- author: Robin Schmidiger
- version: 0.9
- date: 30 December 2023

=================

<a id="brel.networks.calculation_network_node.CalculationNetworkNode"></a>

## CalculationNetworkNode Objects

```python
class CalculationNetworkNode(INetworkNode)
```

Class for representing a node in a network.
Since a node can have children, nodes can also be viewed as trees.

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.get_report_element"></a>

#### get\_report\_element

```python
def get_report_element() -> IReportElement
```

**Returns**:

`IReportElement`: report element associated with this node.
Use the `points_to()` method to check if this node points to a report element.

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.get_resource"></a>

#### get\_resource

```python
def get_resource() -> IResource
```

Would return the resource associated with this node, but calculation network nodes do not point to resources

**Raises**:

- `ValueError`: CalculationNetworkNode does not point to a resource

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.get_fact"></a>

#### get\_fact

```python
def get_fact() -> Fact
```

Would return the fact associated with this node, but calculation network nodes do not point to facts

**Raises**:

- `ValueError`: CalculationNetworkNode does not point to a fact

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.points_to"></a>

#### points\_to

```python
def points_to() -> str
```

**Returns**:

`str`: returns 'report element'

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.get_weight"></a>

#### get\_weight

```python
def get_weight() -> float
```

**Returns**:

`float`: Returns the weight of this node

<a id="brel.networks.calculation_network_node.CalculationNetworkNode.get_concept"></a>

#### get\_concept

```python
def get_concept() -> Concept
```

CalculationNetworkNodes are only associated with concepts

**Returns**:

`Concept`: The concept associated with this node

<a id="brel.networks.calculation_network"></a>

# brel.networks.calculation\_network

This module contains the class for representing a calculation network.
A calculation network is a network of nodes that represent the calculation of a Component.
Calculation networks also contain helper functions for checking the consistency of the calculation network specifically.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 29 December 2023

====================

<a id="brel.networks.calculation_network.CalculationNetwork"></a>

## CalculationNetwork Objects

```python
class CalculationNetwork(INetwork)
```

The class for representing a calculation network.
A calculation network is a network of nodes that indicate which concepts are calculated from which other concepts.

<a id="brel.networks.calculation_network.CalculationNetwork.is_balance_consisent"></a>

#### is\_balance\_consisent

```python
def is_balance_consisent() -> bool
```

Returns true if the network is balance consistent.

A network is balance consistent iff, for each parent-child relationship
- if the two concepts have the same balance (credit/credit or debit/debit), then the child weight must be positive
- if the two concepts have different balances (credit/debit or debit/credit), then the child weight must be negative

**Returns**:

`bool`: True iff the network is balance consistent

<a id="brel.networks.calculation_network.CalculationNetwork.is_aggregation_consistent"></a>

#### is\_aggregation\_consistent

```python
def is_aggregation_consistent(facts: list[Fact]) -> bool
```

A calculation network is aggregation consistent iff for concepts of nodes, the sum of the fact values of the children equals the fact value of the parent.

If there are multiple facts for a concept, but the facts have different dates, then aggregation consistency is checked for each date separately.
This not only holds for the date aspect, but for all aspects of the fact.

**Arguments**:

- `facts`: the facts of the filing against which to check the aggregation consistency

**Returns**:

`bool`: True iff the network is aggregation consistent

