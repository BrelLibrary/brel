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

import pandas as pd
from pyspark import sql
from typing import Any, cast

from brel import Component, Fact, QName
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

    # first class citizens
    def get_all_facts(self) -> list[Fact]:
        """
        :return list[Fact]: a list of all [`Fact`](../facts/facts.md) objects in the filing.
        """
        return self.__context.get_fact_repository().get_all()

    def get_all_report_elements(self) -> list[IReportElement]:
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

    def get_errors(self) -> list[Exception]:
        """
        :return list[Exception]: a list of all errors that occurred during parsing.
        """
        return self.__context.get_error_repository().get_all()

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

    def get_all_reported_concepts(self) -> list[Concept]:
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

    def get_facts_by_concept_name(self, concept_name: QName | str) -> list[Fact]:
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

    def get_facts_by_concept(self, concept: Concept) -> list[Fact]:
        """
        Returns all facts that are associated with a concept.
        :param concept: the concept to get facts for.
        :returns list[Fact]: the list of facts
        """
        return self.get_facts_by_concept_name(concept.get_name())

    def get_all_component_uris(self) -> list[str]:
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

    def generate_fact_table_pandas_df(self) -> pd.DataFrame:
        """
        Converts the filing to a pandas DataFrame.
        :return pandas.DataFrame: the filing as a pandas DataFrame.
        """
        import pandas as pd

        data: list[dict[str, Any]] = []
        for fact in self.get_all_facts():
            d = fact.convert_to_dict()
            data.append(d)

        df = pd.DataFrame(data)
        return df

    def generate_fact_table_spark_df(self) -> tuple[sql.DataFrame, sql.SparkSession]:
        """
        Converts the filing to a spark DataFrame.
        :return pyspark.sql.DataFrame: the filing as a spark DataFrame.
        """
        spark = sql.SparkSession.builder.getOrCreate()
        df = self.generate_fact_table_pandas_df()
        # spark.parallelize()
        return spark.createDataFrame(df), spark

    def generate_components_as_pandas_df(self) -> pd.DataFrame:
        """
        Converts the components to a pandas DataFrame.
        :return pandas.DataFrame: the components as a pandas DataFrame.
        """
        data: list[dict[str, Any]] = []
        for component in self.get_all_components():
            d = component.convert_to_dict()
            data.append(d)

        df = pd.DataFrame(data)
        return df

    def get_all_labels(self) -> list[dict[str, str]]:
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

    def generate_report_elements_as_pandas_df(self) -> pd.DataFrame:
        """
        Converts the report elements to a pandas DataFrame.
        :return pandas.DataFrame: the report elements as a pandas DataFrame.
        """
        data = []
        for re in self.get_all_report_elements():
            d = re.convert_to_dict()
            data.append(d)

        df = pd.DataFrame(data)
        return df
