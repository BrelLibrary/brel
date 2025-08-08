from abc import ABC, abstractmethod

from brel.brel_context import Context


class ContextRepository(ABC):
    @abstractmethod
    def get_context_copy(self, context_id: str) -> Context:
        pass

    @abstractmethod
    def insert_context(self, context: Context) -> None:
        pass
