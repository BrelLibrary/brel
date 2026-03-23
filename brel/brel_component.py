"""
This module contains the Component class.
Components are used to define the presentation, calculation and definition networks of a filing.

Intuitively, they function as the chapters of a report or filing. Note that XBRL sometimes calls
components 'roles'.

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

- get the [`PresentationNetwork`](#./networks/presentation_network.md) using the
`Component.get_presentation_network()` method.
- get the [`CalculationNetwork`](#./networks/calculation_network.md) using the
`Component.get_calculation_network()` method.
- get the [`DefinitionNetwork`](#./networks/definition_network.md) using the
`Component.get_definition_network()` method.

You can print them using the `pprint_network` function in the `brel` module:

```python
from brel import pprint

calculation_network = my_component.get_calculation_network()
pprint(calculation_network)
```

====================

- author: Robin Schmidiger
- version: 0.7
- date: 30 January 2024

====================
"""

from typing import Any, Dict, List, Optional, cast
from brel import Fact
from brel.networks import (
    CalculationNetwork,
    DefinitionNetwork,
    PresentationNetwork,
    INetwork,
)
from brel.services.translation.translation_service import TranslationService


class Component:
    """
    This class implements XBRL components, which are sometimes also called roles.
    Components are used to define the presentation, calculation and definition networks of a filing.
    Intuitively, they function as the chapters of a report or filing.

    A component consists of the following:

    - a URI, also called the roleURI. This is the identifier of the component.
    - an info, also called the definition. This is a string that describes the component.
    It is optional.
    - a set of networks. The most notable kind of networks are the presentation, calculation and
    definition networks.

    """

    def __init__(
        self,
        uri: str,
        info: str,
        presentation_network: Optional[PresentationNetwork] = None,
        calculation_network: Optional[CalculationNetwork] = None,
        definition_network: Optional[DefinitionNetwork] = None,
    ) -> None:
        self.__uri: str = uri
        self.__info: str = info
        self.__presentation_network: Optional[PresentationNetwork] = (
            presentation_network
        )
        self.__calculation_network: Optional[CalculationNetwork] = calculation_network
        self.__definition_network: Optional[DefinitionNetwork] = definition_network

    # first class citizens
    def get_URI(self) -> str:
        """
        :returns str: the URI of the component
        """
        return self.__uri

    def get_info(self) -> str:
        """
        :returns str: the info/definition of the component.
        """
        return self.__info

    def get_presentation_network(self) -> PresentationNetwork | None:
        """
        :returns PresentationNetwork: the presentation network of the component. None if the
        component has no presentation network or if the network is empty.
        """
        return self.__presentation_network

    def get_calculation_network(self) -> CalculationNetwork | None:
        """
        :returns CalculationNetwork: the calculation network of the component. None if the
        component has no calculation network or if the network is empty.
        """
        return self.__calculation_network

    def get_definition_network(self) -> DefinitionNetwork | None:
        """
        :returns DefinitionNetwork: the definition network of the component. None if the component
        has no definition network or if the network is empty.
        """
        return self.__definition_network

    # second class citizens
    def has_presentation_network(self) -> bool:
        """
        :returns bool: True if the component has a presentation network, False otherwise
        """
        return self.__presentation_network != None

    def has_calculation_network(self) -> bool:
        """
        :returns bool: True if the component has a calculation network, False otherwise
        """
        return self.__calculation_network != None

    def has_definition_network(self) -> bool:
        """
        :returns bool: True if the component has a definition network, False otherwise
        """
        return self.__definition_network != None

    def __str__(self) -> str:
        """
        :returns str: a string representation of the component
        """
        return f"Component(id='{self.__uri}', definition='{self.__info}', presentation_network={self.__presentation_network}, calculation_network={self.__calculation_network}, definition_network={self.__definition_network})"

    # The following methods are validating the calculation of the component
    def is_aggregation_consistent(self, facts: list[Fact]) -> bool:
        """
        :param facts: the facts of the filing
        :returns bool: True if and only if the component is aggregation consistent against the given facts
        """
        raise NotImplementedError()

    def get_networks(self) -> list[INetwork]:
        """
        :returns list[INetwork]: the networks of the component
        """
        networks: list[INetwork] = []
        if self.__presentation_network is not None:
            networks.append(self.__presentation_network)
        if self.__calculation_network is not None:
            networks.append(self.__calculation_network)
        if self.__definition_network is not None:
            networks.append(self.__definition_network)
        return networks

    def convert_to_dict(
        self,
        languages: Optional[List[str]] = None,
        translation_service: Optional[TranslationService] = None,
    ) -> Dict[str, Any]:
        """
        :returns dict: a dictionary representation of the component
        """

        if not languages or not translation_service:
            return {
                "network-identifier": self.__uri,
                "info": self.__info,
                "presentation-network": (
                    True if self.__presentation_network is not None else False
                ),
                "calculation-network": (
                    True if self.__calculation_network is not None else False
                ),
                "definintion-network": (
                    True if self.__definition_network is not None else False
                ),
            }

        network_identifier_literal = translation_service.get(
            "literal:network-identifier", languages
        )
        info_literal = translation_service.get("literal:info", languages)

        presentation_network_literal = translation_service.get(
            "literal:presentation-network", languages
        )
        presentation_network = translation_service.get(
            "boolean:" + str(self.__presentation_network is not None).lower(), languages
        )

        calculation_network_literal = translation_service.get(
            "literal:calculation-network", languages
        )
        calculation_network = translation_service.get(
            "boolean:" + str(self.__calculation_network is not None).lower(), languages
        )

        definition_network_literal = translation_service.get(
            "literal:definition-network", languages
        )
        defintion_network = translation_service.get(
            "boolean:" + str(self.__definition_network is not None).lower(), languages
        )

        return {
            network_identifier_literal: self.__uri,
            info_literal: self.__info,
            presentation_network_literal: presentation_network,
            calculation_network_literal: calculation_network,
            definition_network_literal: defintion_network,
        }
