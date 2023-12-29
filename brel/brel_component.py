"""
This module contains the Component class.
Components are used to define the presentation, calculation and definition networks of a filing.
Intuitively, they function as the chapters of a report or filing.

@author: Robin Schmidiger
@version: 0.5
@date: 19 December 2023
"""

from brel import Fact
from brel.networks import PresentationNetwork, CalculationNetwork, DefinitionNetwork


class Component:
    """
    Implements XBRL components, which are sometimes also called roles.
    Components are used to define the presentation, calculation and definition networks of a filing.
    Intuitively, they function as the chapters of a report or filing.
    """

    def __init__(
        self,
        uri: str,
        info: str,
        presentation_network: None | PresentationNetwork = None,
        calculation_network: None | CalculationNetwork = None,
        definition_network: None | DefinitionNetwork = None,
    ) -> None:
        """
        Creates a new Component.
        :param uri: the URI of the component
        :param info: the info/definition of the component.
        :param presentation_network: the presentation network of the component. None if the component has no presentation network or if the network is empty.
        :param calculation_network: the calculation network of the component. None if the component has no calculation network or if the network is empty.
        :param definition_network: the definition network of the component. None if the component has no definition network or if the network is empty.
        """

        self.__uri = uri
        self.__info = info
        self.__presentation_network = presentation_network
        self.__calculation_network = calculation_network
        self.__definition_network = definition_network

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

    def get_presentation(self) -> PresentationNetwork | None:
        """
        :returns PresentationNetwork: the presentation network of the component. None if the component has no presentation network or if the network is empty.
        """
        return self.__presentation_network

    def get_calculation(self) -> CalculationNetwork | None:
        """
        :returns CalculationNetwork: the calculation network of the component. None if the component has no calculation network or if the network is empty.
        """
        return self.__calculation_network

    def get_definition(self) -> DefinitionNetwork | None:
        """
        :returns DefinitionNetwork: the definition network of the component. None if the component has no definition network or if the network is empty.
        """
        return self.__definition_network

    # second class citizens
    def has_presentation(self) -> bool:
        """
        :returns bool: True if the component has a presentation network, False otherwise
        """
        return self.__presentation_network != None

    def has_calculation(self) -> bool:
        """
        :returns bool: True if the component has a calculation network, False otherwise
        """
        return self.__calculation_network != None

    def has_definition(self) -> bool:
        """
        :returns bool: True if the component has a definition network, False otherwise
        """
        return self.__info != ""

    def __str__(self) -> str:
        """
        :returns str: a string representation of the component
        """
        return f"Component(id='{self.__uri}', definition='{self.__info}', presentation_network={self.__presentation_network}, calculation_network={self.__calculation_network}, definition_network={self.__definition_network})"

    # The following methods are validating the calculation of the component
    def is_aggregation_consistent(self, facts: list[Fact]) -> bool:
        """
        :param facts: the facts of the filing
        :returns bool: True iff the components
        """
        # TODO: implement
        raise NotImplemented
