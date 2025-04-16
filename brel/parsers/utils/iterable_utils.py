"""
====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""

from typing import Iterable


def get_first[T](collection: Iterable[T], error_message: str) -> T:
    """
    Get the first element of a collection, or raise an error if the collection is empty.
    :param collection: The collection to get the first element from.
    :param error_message: The error message to raise if the collection is empty.
    :returns: The first element of the collection.
    :raises ValueError: If the collection is empty.
    """
    if not collection:
        raise ValueError(error_message)
    return next(iter(collection))
