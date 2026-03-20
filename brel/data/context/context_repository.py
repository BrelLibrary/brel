from abc import ABC, abstractmethod
from typing import Optional

from brel.brel_context import Context


class ContextRepository(ABC):
    @abstractmethod
    def get_context_copy(self, context_id: str) -> Optional[Context]:
        pass

    @abstractmethod
    def insert_context(self, context: Context) -> bool:
        pass
