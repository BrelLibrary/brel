"""

Brel operates on XBRL filings and represents them as a #Filing object.
This module contains the Filing class.

Filings can be loaded from a folder, a zip file, or one or multiple xml files.

- If a folder is given, then all xml files in the folder are loaded.
- If a zip file is given, then the zip file is extracted to a folder 
and then all xml files in the folder are loaded.
- If one or more xml files are given, then only those xml files are loaded.
- A URI can also be given. In this case, the file is downloaded and cached in a folder.

Note that Brel currently only supports XBRL filings in the form of XML files.

Example usage:

```
from brel import Filing

# open apples 2023 Q3 10-Q filing
filing1 = Filing.open("https://www.sec.gov/Archives/edgar/data/320193/000032019323000077/aapl-20230701_htm.xml")

filing2 = Filing.open("my_folder/")

filing3 = Filing.open("my_file.xml", "my_file2.xml")

# get the facts reporting against us-gaap:Assets
assets_facts = filing1.get_facts_by_concept_name("us-gaap:Assets")
pprint_facts(assets_facts)

```

Note that opening a filing can take **a couple of seconds** depending on the size of the filing.

Once a filing is loaded, it can be queried for its facts, report elements, networks and components.

====================

- author: Robin Schmidiger
- version: 0.7
- date: 12 May 2025

====================
"""

import os
import pandas as pd
from pyspark import sql
from typing import Any, List, Optional, Unpack, cast

from brel import Component, Fact, QName

from brel.errors.area import Area
from brel.errors.error_instance import ErrorInstance
from brel.errors.severity import Severity
from brel.networks import INetwork
from brel.parsers.filing_parser_factory import FilingParserFactory
from brel.parsers.path_loaders.factory import create_path_loader_resolver
from brel.parsers.utils.iterable_utils import exactly_one
from brel.qnames.qname_search_params import QNameSearchParams
from brel.reportelements import (
    Abstract,
    Concept,
    Dimension,
    Hypercube,
    IReportElement,
    LineItems,
    Member,
)
from brel.contexts.filing_context import FilingContext
from brel.config.brel_config import BrelConfig
from brel.services.translation.output_params import OutputParams


class Filing:
    """
    Represents an XBRL filing in the Open Information Model.
    """

    @classmethod
    def open(cls, path: str) -> "Filing":
        path_loader_resolver = create_path_loader_resolver()
        file_paths: list[str] = []
        try:
            path_loader = path_loader_resolver.get_path_loader(path)
            file_paths = path_loader.load(path)
        except ValueError:
            raise ValueError(f"Path {path} is not a valid path")

        parser = FilingParserFactory().create_parser(file_paths)
        context = parser.parse()
        return cls(context)

    def __init__(self, context: FilingContext) -> None:
        self.__context = context
        self.__output_params = OutputParams()

    def get_preferred_languages(
        self,
        function_languages: Optional[str | list[str]],
        allow_report_language: bool,
        allow_system_language: bool,
        allow_default: bool,
    ) -> List[str]:
        if function_languages is None:
            function_languages = []
        elif isinstance(function_languages, str):
            function_languages = [function_languages]

        preferred_filing_languages = self.__output_params.get("languages") or []
        if isinstance(preferred_filing_languages, str):
            preferred_filing_languages = [preferred_filing_languages]

        library_languages = BrelConfig.get_preferred_library_languages() or []
        if isinstance(library_languages, str):
            library_languages = [library_languages]

        sys_language = BrelConfig.get_system_language()
        sys_language_list = (
            [sys_language] if sys_language and allow_system_language else []
        )

        available_filing_languages = (
            self.__context.get_available_filing_languages()
            if allow_report_language
            else []
        )

        all_languages = (
            function_languages
            + preferred_filing_languages
            + library_languages
            + sys_language_list
            + available_filing_languages
        )

        if allow_default:
            all_languages.append("")

        existing_language_set = set()
        all_languages_deduplicated = []
        for language in all_languages:
            if language not in existing_language_set:
                existing_language_set.add(language)
                all_languages_deduplicated.append(language)

        return all_languages_deduplicated

    # first class citizens
    def get_all_facts(self) -> list[Fact]:
        """
        :return list[Fact]: a list of all [`Fact`](../facts/facts.md) objects in the filing.
        """
        return self.__context.get_fact_repository().get_all()

    def get_all_report_elements(self) -> List[IReportElement]:
        """
        :return list[IReportElement]: a list of all [`IReportElement`](../report-elements/report-elements.md) objects in the filing.
        """
        return self.__context.get_report_element_repository().get_all()

    def get_all_components(self) -> list[Component]:
        """
        :return list[Component]: a list of all [`Component`](../components/components.md) objects in the filing.
        Note: components are sometimes called "roles" in the XBRL specification.
        """
        return self.__context.get_component_repository().get_all()

    def get_all_physical_networks(self) -> list[INetwork]:
        """
        Get all [`INetwork`](../components/networks.md) objects in the filing, where network.is_physical() is True.
        :return list[INetwork]: a list of all physical networks in the filing.
        """
        return [
            network
            for network in self.__context.get_network_repository().get_all()
            if network.is_physical()
        ]

    def has_any_errors(self) -> bool:
        return len(self.__context.get_error_repository().get_all()) > 0

    def get_all_errors(self) -> list[ErrorInstance]:
        """
        :returns list[Exception]: a list of all errors (any severity) that occurred during parsing.
        """
        return self.__context.get_error_repository().get_all()

    def get_errors_by_area(self, area: Area) -> list[ErrorInstance]:
        """
        :param Area area: the area of the errors to return
        :returns list[Exception]: a list of all errors with the specified area that occurred during parsing.
        """
        all_errors = self.__context.get_error_repository().get_all()
        area_errors = [error for error in all_errors if error.get_area() == area]
        return area_errors

    def get_errors_by_severity(self, severity: Severity) -> List[ErrorInstance]:
        """
        :param Severity severity: the severity of the errors to return
        :returns list[Exception]: a list of all errors with the specified severity that occurred during parsing.
        """
        return self.__context.get_error_repository().get_by_severity(severity)

    def get_errors(self) -> List[ErrorInstance]:
        """
        :returns list[Exception]: a list of all errors (severity = ERROR) that occurred during parsing.
        """
        return self.get_errors_by_severity(Severity.ERROR)

    def get_warnings(self) -> List[ErrorInstance]:
        """
        :returns list[Exception]: a list of all warnings (severity = WARNING) that occurred during parsing.
        """
        return self.get_errors_by_severity(Severity.WARNING)

    def get_infos(self) -> List[ErrorInstance]:
        """
        :returns list[Exception]: a list of all infos (severity = INFO) that occurred during parsing.
        """
        return self.get_errors_by_severity(Severity.INFO)

    # second class citizens
    def get_all_concepts(self) -> list[Concept]:
        """
        :returns list[Concept]: a list of all concepts in the filing.
        Note that concepts are defined according to the Open Information Model. They are not the same as abstracts, line items, hypercubes, dimensions, or members.
        """
        return cast(
            list[Concept],
            list(
                filter(lambda x: isinstance(x, Concept), self.get_all_report_elements())
            ),
        )

    def get_all_abstracts(self) -> list[Abstract]:
        """
        :returns list[Abstract]: a list of all abstracts in the filing.
        """
        return cast(
            list[Abstract],
            list(
                filter(
                    lambda x: isinstance(x, Abstract), self.get_all_report_elements()
                )
            ),
        )

    def get_all_line_items(self) -> list[LineItems]:
        """
        :returns list[LineItems]: a list of all line items in the filing.
        """
        return cast(
            list[LineItems],
            list(
                filter(
                    lambda x: isinstance(x, LineItems), self.get_all_report_elements()
                )
            ),
        )

    def get_all_hypercubes(self) -> list[Hypercube]:
        """
        :returns list[Hypercube]: a list of all hypercubes in the filing.
        """
        return cast(
            list[Hypercube],
            list(
                filter(
                    lambda x: isinstance(x, Hypercube), self.get_all_report_elements()
                )
            ),
        )

    def get_all_dimensions(self) -> list[Dimension]:
        """
        :returns list[Dimension]: a list of all dimensions in the filing.
        """
        return cast(
            list[Dimension],
            list(
                filter(
                    lambda x: isinstance(x, Dimension), self.get_all_report_elements()
                )
            ),
        )

    def get_all_members(self) -> list[Member]:
        """
        :returns list[Member]: a list of all members in the filing.
        """
        return cast(
            list[Member],
            list(
                filter(lambda x: isinstance(x, Member), self.get_all_report_elements())
            ),
        )

    def get_report_element_by_name(
        self, element_qname: QName | str
    ) -> IReportElement | None:
        """
        :param element_qname: the name of the report element to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns IReportElement|None: the report element with the given name. If no report element is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(element_qname, str):
            search_params = QNameSearchParams.from_string(element_qname)
            return exactly_one(
                self.__context.get_report_element_service().get_fuzzy(search_params),
                f"Report element with name {element_qname} not found in filing",
            )
        else:
            return self.__context.get_report_element_repository().get_by_qname(
                element_qname
            )

    def get_concept_by_name(self, concept_qname: QName | str) -> Concept:
        """
        :param concept_qname: the name of the concept to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns Concept|None: the concept with the given name. If no concept is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(concept_qname, str):
            search_params = QNameSearchParams.from_string(concept_qname)
            return exactly_one(
                self.__context.get_report_element_service().get_fuzzy_typed(
                    search_params, Concept
                ),
                f"Concept with name {concept_qname} not found in filing",
            )
        else:
            return self.__context.get_report_element_repository().get_typed_by_qname(
                concept_qname, Concept
            )

    def get_concept(self, concept_qname: QName | str) -> Concept:
        """
        Alias of `filing.get_concept_by_name(concept_qname)`.
        """
        return self.get_concept_by_name(concept_qname)

    def get_all_reported_concepts(self) -> List[Concept]:
        """
        Returns all concepts that have at least one fact reporting against them.
        :returns list[Concept]: The list of concepts
        """
        reported_concepts: list[Concept] = []
        for fact in self.get_all_facts():
            concept = fact.get_concept().get_value()
            if concept not in reported_concepts:
                reported_concepts.append(concept)

        return reported_concepts

    def get_facts_by_concept_name(self, concept_name: QName | str) -> List[Fact]:
        """
        Returns all facts that are associated with the concept with name concept_name.
        :param concept_name: The name of the concept to get facts for. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns list[Fact]: the list of facts
        :raises ValueError: if the QName string but is not a valid QName or if the prefix is not found.
        """
        if isinstance(concept_name, str):
            search_params = QNameSearchParams.from_string(concept_name)
            concept = exactly_one(
                self.__context.get_report_element_service().get_fuzzy_typed(
                    search_params, Concept
                ),
                f"Concept with name {concept_name} not found in filing",
            )
        else:
            concept = self.__context.get_report_element_repository().get_typed_by_qname(
                concept_name, Concept
            )

        return [
            fact
            for fact in self.get_all_facts()
            if fact.get_concept().get_value() == concept
        ]

    def get_facts_by_concept(self, concept: Concept) -> List[Fact]:
        """
        Returns all facts that are associated with a concept.
        :param concept: the concept to get facts for.
        :returns list[Fact]: the list of facts
        """
        return self.get_facts_by_concept_name(concept.get_name())

    def get_all_component_uris(self) -> List[str]:
        """
        :return list[str]: a list of all component URIs in the filing.
        """
        return [component.get_URI() for component in self.get_all_components()]

    def get_component(self, uri: str) -> Component:
        """
        :param URI: the URI of the component to get.
        :return Component|None: the component with the given URI. None if no component is found.
        """
        component = next(
            (comp for comp in self.get_all_components() if comp.get_URI() == uri), None
        )
        if component is None:
            raise ValueError(f"Component with URI {uri} not found")
        else:
            return component

    def generate_fact_table_pandas_df(
        self, **kwargs: Unpack[OutputParams]
    ) -> pd.DataFrame:
        """
        Converts the filing to a pandas DataFrame.
        :return pandas.DataFrame: the filing as a pandas DataFrame.
        """
        return self.__generate_pandas_df_from_elements(self.get_all_facts(), **kwargs)

    def generate_fact_table_spark_df(self) -> tuple[sql.DataFrame, sql.SparkSession]:
        """
        Converts the filing to a spark DataFrame.
        :return pyspark.sql.DataFrame: the filing as a spark DataFrame.
        """
        spark = sql.SparkSession.builder.getOrCreate()
        df = self.generate_fact_table_pandas_df()
        # spark.parallelize()
        return spark.createDataFrame(df), spark

    def generate_components_as_pandas_df(
        self, **kwargs: Unpack[OutputParams]
    ) -> pd.DataFrame:
        """
        Converts the components to a pandas DataFrame.
        :return pandas.DataFrame: the components as a pandas DataFrame.
        """
        return self.__generate_pandas_df_from_elements(
            self.get_all_components(), **kwargs
        )

    def get_all_labels(self) -> List[dict[str, str]]:
        """
        :return list[dict[str, str]]: a list of all labels in the filing.
        """
        labels = []
        for re in self.get_all_report_elements():
            if isinstance(re, IReportElement):
                for label in re.get_labels():
                    labeldict = label.convert_to_dict()
                    labeldict["report_element"] = re.get_name()
                    labels.append(labeldict)
        return labels

    def generate_labels_as_pandas_df(self) -> pd.DataFrame:
        """
        Converts the labels to a pandas DataFrame.
        :return pandas.DataFrame: the labels as a pandas DataFrame.
        """
        data = self.get_all_labels()
        df = pd.DataFrame(data)
        return df

    def generate_report_elements_as_pandas_df(
        self, **kwargs: Unpack[OutputParams]
    ) -> pd.DataFrame:
        """
        Converts the report elements to a pandas DataFrame.
        :return pandas.DataFrame: the report elements as a pandas DataFrame.
        """
        return self.__generate_pandas_df_from_elements(
            self.get_all_report_elements(), **kwargs
        )

    def __generate_pandas_df_from_elements(
        self,
        elements: List[IReportElement] | List[Component] | List[Fact],
        **kwargs: Unpack[OutputParams],
    ) -> pd.DataFrame:
        output_params = self.__infer_output_params(**kwargs)
        data = []

        translation_service = self.__context.get_translation_service()
        translation_service.set_match_locale(output_params["match_locale"])

        if output_params["allow_mixed"]:
            for element in elements:
                languages = output_params["languages"]
                languages_list = (
                    languages if isinstance(languages, list) else [languages]
                )

                d = element.convert_to_dict(languages_list, translation_service)
                data.append(d)
        else:
            for language in output_params["languages"]:
                for element in elements:
                    try:
                        d = element.convert_to_dict([language], translation_service)
                        data.append(d)
                    except:
                        data = []
                        break

        df = pd.DataFrame(data)
        return df

    def get_preferred_output_parameter(
        self, passed_value: Optional[bool], parameter_name: str
    ) -> bool:
        if passed_value is not None:
            return passed_value

        filing_value = cast(bool, self.__output_params.get(parameter_name))
        if filing_value is not None:
            return filing_value

        config_value = BrelConfig.get_boolean_output_parameter_by_name(parameter_name)
        if config_value is not None:
            return config_value

        return False

    def __infer_output_params(self, **kwargs: Unpack[OutputParams]) -> OutputParams:
        allow_default = self.get_preferred_output_parameter(
            kwargs.get("allow_default"), "allow_default"
        )

        allow_system_language = self.get_preferred_output_parameter(
            kwargs.get("allow_system_language"), "allow_system_language"
        )

        allow_report_language = self.get_preferred_output_parameter(
            kwargs.get("allow_report_language"), "allow_report_language"
        )

        match_locale = self.get_preferred_output_parameter(
            kwargs.get("match_locale"), "match_locale"
        )

        allow_mixed = self.get_preferred_output_parameter(
            kwargs.get("allow_mixed"), "allow_mixed"
        )

        languages = self.get_preferred_languages(
            kwargs.get("languages"),
            allow_system_language,
            allow_report_language,
            allow_default,
        )

        return OutputParams(
            {
                "languages": languages,
                "allow_default": allow_default,
                "allow_system_language": allow_system_language,
                "allow_report_language": allow_report_language,
                "match_locale": match_locale,
                "allow_mixed": allow_mixed,
            }
        )

    def set_filing_output_params(self, **kwargs: Unpack[OutputParams]) -> None:
        self.__output_params = kwargs

    @classmethod
    def set_global_output_params(self, **kwargs: Unpack[OutputParams]) -> None:
        BrelConfig.set_library_output_parameters(**kwargs)
