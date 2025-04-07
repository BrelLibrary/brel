from abc import ABC, abstractmethod
from typing import Union

class IResource(ABC):
    @abstractmethod
    def get_label(self) -> str:  # pragma: no cover
        """
        Get the label of the resource
        :returns str: the label of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_role(self) -> Union[str, None]:  # pragma: no cover
        """
        Get the role of the resource
        :returns str|None: the role of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_title(self) -> Union[str, None]:  # pragma: no cover
        """
        Get the title of the resource
        :returns str|None: the title of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_content(self) -> Union[dict, list, str, None]:  # pragma: no cover
        """
        Get the content of the resource
        :returns dict|list|str|None: the content of the resource.
        """
        raise NotImplementedError
