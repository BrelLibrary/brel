<a id="brel.networks.i_network"></a>

# brel.networks.i\_network

Networks in XBRL are used to define relationships between different things in a filing.
For example

- Presentation networks define a hierarchy of report elements
- Calculation networks define which concepts should be the sum of which other concepts
- Definition networks define what the relationship between the types of the report elements are
- Label networks establish relationships between report elements and human readable labels
- Reference networks establish a link between report elements and other resources such as websites or documents

All networks in brel are represented by the INetwork interface.

Since only the calculation network has any special functionality thus far, the other networks are not part of this documentation.
They are all implemented in the same way as the calculation network and can be inspected using their shared interface INetwork.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 07 January 2024

====================

<a id="brel.networks.i_network.INetwork"></a>

## INetwork Objects

```python
class INetwork(ABC)
```

Interface for representing networks in Brel.
The networks are defined according to the XBRL Generic Links 1.0 specification
available [HERE](https://www.xbrl.org/specification/gnl/rec-2009-06-22/gnl-rec-2009-06-22.html)

<a id="brel.networks.i_network.INetwork.get_roots"></a>

#### get\_roots

```python
def get_roots() -> list[INetworkNode]
```

Get all root nodes of the network

**Returns**:

`list[NetworkNode]`: representing the root nodes of the network.

<a id="brel.networks.i_network.INetwork.get_link_role"></a>

#### get\_link\_role

```python
def get_link_role() -> str
```

Get the link role of the network

**Returns**:

`str`: containing the link role of the network.
Note: This returns the same as `get_URL()` on the parent component

<a id="brel.networks.i_network.INetwork.get_link_name"></a>

#### get\_link\_name

```python
def get_link_name() -> QName
```

Get the link name of the network

**Returns**:

`QName`: link name of the network. e.g. for presentation networks this is usually "link:presentationLink"

<a id="brel.networks.i_network.INetwork.is_physical"></a>

#### is\_physical

```python
def is_physical() -> bool
```

Check if the network is a physical network

Physical networks must have the same link/arc role/name across all nodes

**Returns**:

`bool`: indicating if the network is a physical network

<a id="brel.networks.i_network.INetwork.get_arc_roles"></a>

#### get\_arc\_roles

```python
def get_arc_roles() -> list[str]
```

Get all the arc roles that are used by nodes in the network

**Returns**:

`list[str]`: list of all arc roles that are used by nodes in the network

<a id="brel.networks.i_network.INetwork.get_arc_name"></a>

#### get\_arc\_name

```python
def get_arc_name() -> QName | None
```

Get the arc name of all the arcs in the network. All arcs in the network have the same arc name.

**Returns**:

`QName|None`: The arc name of all the arcs in the network. Returns None if the network is empty.

<a id="brel.networks.i_network.INetwork.get_root"></a>

#### get\_root

```python
def get_root() -> INetworkNode
```

Get the root node of the network if the network has only one root.

Note that each network must have at least one root node.

**Raises**:

- `ValueError`: if the network has multiple roots

**Returns**:

`NetworkNode`: representing the root node of the network.

<a id="brel.networks.i_network.INetwork.get_all_nodes"></a>

#### get\_all\_nodes

```python
def get_all_nodes() -> list[INetworkNode]
```

Get all nodes in the network as a list

**Returns**:

`list[NetworkNode]`: containing all nodes in the network

