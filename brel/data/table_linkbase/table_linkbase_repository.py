from abc import ABC, abstractmethod
from typing import List, Optional

from brel.table_linkbases.definition_model.table import Table


class TableLinkbaseRepository(ABC):
    @abstractmethod
    def get_all_definition_tables(self) -> List[Table]:
        pass

    @abstractmethod
    def get_definition_table_with_linkrole(self, linkrole: str) -> List[Table]:
        pass

    @abstractmethod
    def upsert_definition_table(self, table: Table) -> None:
        pass
