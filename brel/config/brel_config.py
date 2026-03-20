from locale import getdefaultlocale
from typing import List, Optional, Unpack, cast

from brel.services.translation.output_params import OutputParams


class BrelConfig:
    output_params: OutputParams = OutputParams(
        {
            "languages": [],
            "match_locale": True,
            "allow_mixed": True,
            "allow_default": True,
            "allow_system_language": True,
            "allow_report_language": True,
        }
    )

    @classmethod
    def get_preferred_library_languages(cls) -> List[str] | str:
        return cls.output_params.get("languages") or []

    @classmethod
    def set_preferred_library_languages(cls, languages: str | list[str]):
        if isinstance(languages, str):
            languages = [languages]

        cls.output_params["languages"] = languages

    @classmethod
    def set_library_output_parameters(cls, **kwargs: Unpack[OutputParams]):
        cls.output_params = kwargs

    @classmethod
    def get_boolean_output_parameter_by_name(
        cls, parameter_name: str
    ) -> Optional[bool]:
        return cast(bool, cls.output_params.get(parameter_name))

    @classmethod
    def get_system_language(cls) -> Optional[str]:
        locale, _ = getdefaultlocale()
        return locale

    @classmethod
    def get_translations_filepath(cls) -> str:
        return "./brel/config/translations.csv"
