from abc import ABC, abstractmethod
import lxml
import lxml.etree

class ISchemaManager(ABC):
    @abstractmethod
    def __init__(self, cache_location: str, filing_location: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_schema(self, schema_uri: str) -> lxml.etree._ElementTree:
        raise NotImplementedError
    
    @abstractmethod
    def get_all_schemas(self) -> list[lxml.etree._ElementTree]:
        raise NotImplementedError
    
    @abstractmethod
    def get_schema_names(self) -> list[str]:
        raise NotImplementedError
