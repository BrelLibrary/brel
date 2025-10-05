from typing import Callable, Optional, Self, cast, final
from lxml import etree

from brel.errors.area import Area
from brel.errors.severity import Severity
from brel.qnames.qname import QName


@final
class ErrorInstance:
    def __init__(
        self,
        severity: Severity,
        area: Area,
        numeric_code: str,
        message: str,
        hint: Optional[str] = None,
        xbrl_error_code: Optional[QName] = None,
    ) -> None:
        self.__severity = severity
        self.__area = area
        self.__numeric_code = numeric_code
        self.__message = message
        self.__hint = hint
        self.__xbrl_error_code = xbrl_error_code
        self.__context: Optional[etree._Element] = None

    def update_message(self, **kwargs: Optional[str]):
        try:
            self.__message = self.__message.format(**kwargs)
        except KeyError:
            raise ValueError(
                f"You have not provided the required arguments for the error {str(self.get_full_error_code())}"
            )

    def set_context(self, context: etree._Element):
        self.__context = context

    def get_severity(self):
        return self.__severity

    def get_area(self):
        return self.__area

    def get_numeric_code(self):
        return self.__numeric_code

    def get_message(self):
        return self.__message

    def get_context(self):
        return self.__context

    def get_hint(self):
        return self.__hint

    def get_xbrl_error_code(self):
        return self.__xbrl_error_code

    def get_full_error_code(self):
        xbrl_error_code_string = (
            f" [{self.get_xbrl_error_code().clark_notation()}]"
            if self.get_xbrl_error_code()
            else ""
        )

        return (
            self.__severity.value
            + "-"
            + str(self.__area.value)
            + "-"
            + self.__numeric_code
            + xbrl_error_code_string
        )

    def __str__(self):
        return self.get_full_error_code() + ": " + self.get_message()
