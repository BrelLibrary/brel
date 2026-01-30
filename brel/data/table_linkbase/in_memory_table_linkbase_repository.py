from collections import defaultdict
from typing import List, Optional
from brel.data.table_linkbase.table_linkbase_repository import TableLinkbaseRepository
from brel.table_linkbases.definition_model.table import Table


class InMemoryTableLinkbaseRepository(TableLinkbaseRepository):
    def __init__(self) -> None:
        self.__structural_tables_by_linkrole: dict[str, List[Table]] = defaultdict(
            List[Table]
        )

    def get_all_definition_tables(self) -> List[Table]:
        """
        Returns a list of all definition tables in the repository.
        This method returns all definition tables, regardless of their linkrole.
        :return: A list of all definition tables in the repository.
        :rtype: List[Table]
        """
        return [x for xs in self.__structural_tables_by_linkrole.values() for x in xs]

    def get_definition_table_with_linkrole(self, linkrole: str) -> List[Table]:
        return self.__structural_tables_by_linkrole.get(linkrole) or []

    def upsert_definition_table(self, table: Table) -> None:
        self.__structural_tables_by_linkrole[table.get_linkrole()].append(table)
