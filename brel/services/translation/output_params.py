from typing import List, TypedDict


class OutputParams(TypedDict, total=False):
    languages: str | List[str]
    match_locale: bool
    allow_mixed: bool
    allow_default: bool
    allow_system_language: bool
    allow_report_language: bool
