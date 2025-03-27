"""
Module for pretty printing a component and all its networks to the console.

====================

- author: Robin Schmidiger
- version: 0.1
- date: 03 February 2024

====================
"""

import rich
from brel import Component
from brel.utils import pprint_network


def pprint_component(component: Component):
    """
    Print a component and all its networks to the console.
    """

    # print(f"Component: {component.get_URI()}")
    # print(f"Info: {component.get_info()}")
    rich.print(f"[bold]Component:[/bold] {component.get_URI()}")
    rich.print(f"[italic]Info:[/italic] {component.get_info()}")

    networks = component.get_networks()
    for network in networks:
        pprint_network(network)
        print()

    if len(networks) == 0:
        # print("No networks found.")
        rich.print("[yellow]No networks in this component.[/yellow]")

    print()
