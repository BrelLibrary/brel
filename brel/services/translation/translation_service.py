from collections import defaultdict
import os
from typing import Dict, List, Optional

from brel.config.brel_config import BrelConfig
from brel.qnames.qname import QName

import csv

from brel.resource.brel_label import BrelLabel


class TranslationService:
    def __init__(self):
        self.__translations: Dict[QName, Dict[str, str]] = defaultdict(dict)
        self.__match_locale = True

    def set_match_locale(self, match_locale: bool):
        self.__match_locale = match_locale

    def load_from_csv(self, path: Optional[str] = None, override: bool = True) -> None:
        if override:
            self.__translations = defaultdict(dict)

        if not path:
            path = BrelConfig.get_translations_filepath()

        with open(path, "r", encoding="utf-8") as file:
            csv_file = csv.reader(file)
            header_read = False
            for line in csv_file:
                if not header_read:
                    header_read = True
                    continue

                namespace, localname, language, locale, translation = (
                    line[0],
                    line[1],
                    line[2],
                    line[3],
                    line[4],
                )
                qname = QName(namespace, "", localname)
                self.__translations[qname][(language + "-" + locale)] = translation

    def languages_match(self, requested_language: str, available_language: str):
        requested_language = requested_language.lower()
        available_language = available_language.lower()

        if self.__match_locale:
            return available_language == requested_language
        else:
            requested_language = requested_language.split("-")[0]
            available_language = available_language.split("-")[0]

            return requested_language == available_language

    def get_single(self, qname: QName, language: str) -> str:
        """
        Get the translation for the given qname and language.
        :param qname: the qname of the translation to get
        :param language: the language of the translation to get
        :returns str: the translation
        """
        if language == "":
            return qname.local_name

        language = language.lower()
        if qname not in self.__translations:
            return qname.local_name

        for translation_language, translation in self.__translations[qname].items():
            if self.languages_match(language, translation_language):
                return translation

        raise KeyError(
            f"No suitable translation for {qname.clark_notation()} found for language {language}"
        )

    def get(
        self,
        qname: str | QName,
        languages: str | List[str],
        base: str = "http://www.brel.com/translations/",
    ) -> str:
        """
        Get the translation for the given qname and languages. Falls back on the rest of the languages. If no language is found, throws an error.
        :param qname: the qname of the translation to get
        :param languages: the languages of the translation to get
        :returns str: the translation
        """
        if isinstance(languages, str):
            languages = [languages]

        if isinstance(qname, str):
            split_qname = qname.split(":")
            qname = QName(base + split_qname[0], "", split_qname[1])

        for language in languages:
            try:
                return self.get_single(qname, language)
            except:
                continue

        raise KeyError(
            f"No suitable translation for {qname.clark_notation()} found for languages {languages}"
        )

    def get_from_labels(
        self,
        labels: List[BrelLabel],
        languages: str | List[str],
        default_label: str | BrelLabel= "NO_LABEL",
    ) -> str:
        """
        Select the first label with the given language.
        :param languages: the languages of the label to select
        :returns BrelLabel: the first label with the given language
        """
        if isinstance(languages, str):
            languages = [languages]
        
        if isinstance(default_label, str):
            default_label = BrelLabel(default_label, "", "")
        
        for language in languages:
            label = self.get_label_with_language(labels, language, default_label)
            if label is not None:
                return label.__str__()

        raise ValueError(f"No label found for languages: {languages}")

    def get_label_with_language(
        self, labels: List[BrelLabel], language: str, default_label: BrelLabel
    ) -> Optional[BrelLabel]:
        """
        Get the label with the given language.
        :param language: the language of the label to get
        :returns BrelLabel: the label with the given language
        """
        if language == "":
            return default_label

        for label in labels:
            if self.languages_match(language, label.get_language()):
                return label

        return None
