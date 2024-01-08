<a id="brel.networks.i_network_node"></a>

# brel.networks.i\_network\_node

This module contains the interface for a node in a network.
All nodes in a network are built on a common interface that allows for some basic navigation of the network.
The network node interface also contains some utility methods for working with networks and nodes.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 2023-12-29

====================

<a id="brel.networks.i_network_node.INetworkNode"></a>

## INetworkNode Objects

```python
class INetworkNode(ABC)
```

Interface for representing a node in a network.
Since a node can have children, nodes can also be viewed as trees.

Each node in a network can point to one of the following:

- A report element [IReportElement](#./reportelements/i_report_element.md): use `node.get_report_element()`
- A resource[IResource](#./resource/i_resource.md): use `node.get_resource()`
- A fact[Fact](#./facts/fact.md):

The getter methods above will raise a ValueError if the node does not point to the requested type.
Use the `points_to()` method to check if the node points to a report element, resource or fact.

- If the node points to a report element, `points_to()` will return 'report element'
- If the node points to a resource, `points_to()` will return 'resource'
- If the node points to a fact, `points_to()` will return 'fact'

To navigate the network, use the `get_children()` method to get the children of a node.

Each node also has an order attribute which can be accessed using the `get_order()` method.
The children of a node are ordered by their order attribute.

<a id="brel.networks.i_network_node.INetworkNode.get_report_element"></a>

#### get\_report\_element

```python
@abstractmethod
def get_report_element() -> IReportElement
```

**Raises**:

- `ValueError`: if this node does not point to a report element.
Use the `points_to()` method to check if this node points to a report element.

**Returns**:

`IReportElement`: report element associated with this node.

<a id="brel.networks.i_network_node.INetworkNode.get_resource"></a>

#### get\_resource

```python
@abstractmethod
def get_resource() -> IResource
```

**Raises**:

- `ValueError`: if this node does not point to a resource.
Use the `points_to()` method to check if this node points to a resource.

**Returns**:

`IResource`: resource associated with this node.

<a id="brel.networks.i_network_node.INetworkNode.get_fact"></a>

#### get\_fact

```python
@abstractmethod
def get_fact() -> Fact
```

**Raises**:

- `ValueError`: if this node does not point to a fact.
Use the `points_to()` method to check if this node points to a fact.

**Returns**:

`Fact`: fact associated with this node.

<a id="brel.networks.i_network_node.INetworkNode.points_to"></a>

#### points\_to

```python
@abstractmethod
def points_to() -> str
```

Returns

- 'resource' if this node points to a resource
- 'report element' if this node points to a report element
- 'fact' if this node points to a fact

**Returns**:

`str`: containing 'resource', 'report element' or 'fact'

<a id="brel.networks.i_network_node.INetworkNode.get_children"></a>

#### get\_children

```python
@abstractmethod
def get_children() -> list["INetworkNode"]
```

Returns all children of this node

**Returns**:

`list[NetworkNode]`: list containing the children of this node

<a id="brel.networks.i_network_node.INetworkNode.get_arc_role"></a>

#### get\_arc\_role

```python
@abstractmethod
def get_arc_role() -> str
```

**Returns**:

`str`: the arc role of this node. There can be nodes with different arc roles in the same network.

<a id="brel.networks.i_network_node.INetworkNode.get_arc_name"></a>

#### get\_arc\_name

```python
@abstractmethod
def get_arc_name() -> QName
```

**Returns**:

`QName`: the arc name of this node. All nodes in the same network have the same arc name.

<a id="brel.networks.i_network_node.INetworkNode.get_link_role"></a>

#### get\_link\_role

```python
@abstractmethod
def get_link_role() -> str
```

**Returns**:

`str`: the link role of this node. This is the same as the link role of the network that the node is in.

<a id="brel.networks.i_network_node.INetworkNode.get_link_name"></a>

#### get\_link\_name

```python
@abstractmethod
def get_link_name() -> QName
```

**Returns**:

`QName`: the link name of this node. This is the same as the link name of the network that the node is in.

<a id="brel.networks.i_network_node.INetworkNode.get_all_descendants"></a>

#### get\_all\_descendants

```python
def get_all_descendants() -> list["INetworkNode"]
```

Returns all descendants of the current node

**Returns**:

`list[NetworkNode]`: list containing all descendants of this node

<a id="brel.networks.i_network_node.INetworkNode.is_leaf"></a>

#### is\_leaf

```python
def is_leaf() -> bool
```

**Returns**:

`bool`: True if this node is a leaf, False otherwise

<a id="brel.networks.i_network_node.INetworkNode.get_order"></a>

#### get\_order

```python
@abstractmethod
def get_order() -> float
```

**Returns**:

`float`: The order of this node. Nodes are ordered by their order attribute.

