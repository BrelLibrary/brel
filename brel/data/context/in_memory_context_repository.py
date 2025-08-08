from copy import deepcopy
from typing import Dict
from brel.brel_context import Context
from brel.data.context.context_repository import ContextRepository


class InMemoryContextRepository(ContextRepository):
    def __init__(self):
        self.__contexts = {}

    def get_context_copy(self, context_id: str) -> Context:
        """
        Retrieves a context from the repository by its context id.
        :param context_id: The id of the context to retrieve
        :return: A copy of the context associated with the given context id
        :raises KeyError: If the context id does not exist in the repository
        """
        if context_id not in self.__contexts:
            raise KeyError(f"Context with id {context_id} does not exist.")

        return deepcopy(self.__contexts[context_id])

    def insert_context(self, context: Context) -> None:
        """
        Inserts a context into the repository. If the context id already exists, raises a ValueError
        :param context: The context to be inserted
        :return: The inserted context
        :raises ValueError: If the context id already exists
        """

        context_id = context._get_id()

        if context_id not in self.__contexts:
            self.__contexts[context_id] = context
        else:
            raise ValueError(f"Context with id {context_id} already exists.")
