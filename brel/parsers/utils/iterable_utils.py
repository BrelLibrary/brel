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
    # TODO schmidi: pass ValueError instead of error_message
    if not collection:
        raise ValueError(error_message)
    return next(iter(collection))


def exactly_one[
    T
](
    collection: Iterable[T],
    error_message: str = "Collection must contain exactly one element",
) -> T:
    """
    Get the first element of a collection, or raise an error if the collection is empty or has more than one element.
    :param collection: The collection to get the first element from.
    :param error_message: The error message to raise if the collection is empty or has more than one element.
    :returns: The first element of the collection.
    :raises ValueError: If the collection is empty or has more than one element.
    """
    if not collection:
        raise ValueError(error_message)
    iterator = iter(collection)
    first = next(iterator)
    if next(iterator, None) is not None:
        raise ValueError(error_message)
    return first


def at_most_one[
    T
](
    collection: Iterable[T],
    error_message: str = "Collection must contain at most one element",
) -> (T | None):
    """
    Get the first element of a collection, or return None if the collection is empty or has more than one element.
    :param collection: The collection to get the first element from.
    :param error_message: The error message to raise if the collection has more than one element.
    :returns: The first element of the collection, or None if the collection is empty.
    :raises ValueError: If the collection has more than one element.
    """
    # TODO schmidi: pass ValueError instead of error_message
    iterator = iter(collection)
    first = next(iterator, None)
    if next(iterator, None) is not None:
        raise ValueError(error_message)
    return first
