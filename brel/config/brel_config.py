from locale import getdefaultlocale
from typing import Optional


class BrelConfig:
    preferred_library_languages: list[str] = []

    @classmethod
    def get_preferred_library_languages(cls) -> list[str]:
        return cls.preferred_library_languages

    @classmethod
    def set_preferred_library_languages(cls, languages: str | list[str]):
        if isinstance(languages, str):
            languages = [languages]

        cls.preferred_library_languages = languages

    @classmethod
    def get_system_language(cls) -> Optional[str]:
        locale, _ = getdefaultlocale()
        return locale
