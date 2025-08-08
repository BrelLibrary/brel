from typing import Optional, Self
from lxml import etree

from brel.errors.area import Area
from brel.errors.error_code import ErrorCode
from brel.errors.error_registry import error_registry
from brel.errors.severity import Severity


class ErrorInstance:
    def __init__(
        self,
        severity: Severity,
        area: Area,
        numeric_code: str,
        message: str,
        context: Optional[etree._Element],
        hint: Optional[str],
    ) -> None:
        self.__severity = severity
        self.__area = area
        self.__numeric_code = numeric_code
        self.__message = message
        self.__context = context
        self.__hint = hint

    @classmethod
    def create_error_instance(
        cls,
        error_code: ErrorCode,
        error_context: Optional[etree._Element] = None,
        **kwargs: str,
    ) -> Self:
        error_template = error_registry.get(error_code)

        if not error_template:
            raise ValueError(f"Error code {error_code} is not valid.")

        try:
            formatted_message = str(error_template["message"]).format(**kwargs)
        except KeyError:
            raise ValueError(
                f"You have not provided the required arguments for the error {str(error_code)}"
            )

        error = cls(
            severity=Severity(error_template["severity"]),
            area=Area(error_template["area"]),
            numeric_code=str(error_template["numeric_code"]),
            message=formatted_message,
            context=error_context,
            hint=str(error_template["hint"]) if "hint" in error_template else None,
        )

        return error

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

    def get_full_error_code(self):
        return str(self.__severity) + "-" + str(self.__area) + "-" + self.__numeric_code

    def __str__(self):
        return self.get_full_error_code() + ": " + self.get_message()
