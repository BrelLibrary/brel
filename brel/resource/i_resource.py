from abc import ABC, abstractmethod


class IResource(ABC):
    @abstractmethod
    def get_label(self) -> str:
        """
        Get the label of the resource
        @return: the label of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_role(self) -> str | None:
        """
        Get the role of the resource
        @return: the role of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_title(self) -> str | None:
        """
        Get the title of the resource
        @return: the title of the resource as a string
        """
        raise NotImplementedError

    @abstractmethod
    def get_content(self) -> dict | list | str | None:
        """
        Get the content of the resource
        @return: the content of the resource as a dict
        """
        raise NotImplementedError
