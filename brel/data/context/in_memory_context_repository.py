from copy import deepcopy
from typing import Dict, Optional
from brel.brel_context import Context
from brel.data.context.context_repository import ContextRepository


class InMemoryContextRepository(ContextRepository):
    def __init__(self):
        self.__contexts = {}

    def get_context_copy(self, context_id: str) -> Optional[Context]:
        """
        Retrieves a context from the repository by its context id.
        :param context_id: The id of the context to retrieve
        :return: A copy of the context associated with the given context id or
        None if the context is not found.
        """
        if context_id not in self.__contexts:
            return None

        return deepcopy(self.__contexts[context_id])

    def insert_context(self, context: Context) -> bool:
        """
        Inserts a context into the repository.
        :param context: The context to be inserted
        :return: Whether the context was successfully added
        """

        context_id = context._get_id()

        if context_id not in self.__contexts:
            self.__contexts[context_id] = context
            return True

        return False
