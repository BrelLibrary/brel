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
- version: 0.5
- date: 29 January 2024

====================
"""

import os
import pandas as pd
import zipfile
from pyspark import sql
from typing import Callable, TypeGuard, cast

from brel import Component, Fact, QName
from brel.characteristics import Aspect
from brel.networks import INetwork
from brel.parsers import IFilingParser, XMLFilingParser, XHTMLFilingParser
from brel.reportelements import (
    Abstract,
    Concept,
    Dimension,
    Hypercube,
    IReportElement,
    LineItems,
    Member,
)

DEBUG = False


class Filing:
    """
    Represents an XBRL filing in the Open Information Model.
    """

    @classmethod
    def open(cls, path, mode="xml", *args) -> "Filing":
        """
        Opens a #Filing when given a path. The path can point to one of the following:
        - a folder
        - a zip file
        - an xml file
        - multiple xml files

        Notes:

        - The args parameter is ignored unless the path points to an xml file.
        - Depending on the size of the filing, loading can take **a couple of seconds**.

        :param path: the path to the filing. This can be a folder, an xml file, or a zip file.
        :param mode: the mode to use when opening the filing. This can be "xml" or "xhtml".
        :param args: additional xml files to load. These are only used if the path is an xml file.
        :returns Filing: a #Filing object with the filing loaded.
        :raises ValueError: if the path is not a valid path.
        """

        def search_filetypes(mode: str, filename: str) -> bool:
            """
            Check if a file is of a correct type given the mode.
            :param mode: the mode to use when checking the file type. This can be "xml" or "xhtml".
            :param filename: the name of the file.
            :return bool: True if the file is of the correct type given the mode, False otherwise.
            """
            if mode == "xml":
                return filename.endswith(".xml")
            elif mode == "xhtml":
                return filename.endswith(".xml") or filename.endswith(".htm") or filename.endswith(".html")
            else:
                # Make sure that only a supported mode is used
                raise ValueError("Mode must be 'xml' or 'xhtml'")

        def choose_file_manager(mode: str, files: list[str]) -> IFilingParser:
            """
            Return the correct file manager given the mode.
            :param mode: the mode to use when checking the file type. This can be "xml" or "xhtml".
            :param files: the list of files.
            :return IFilingParser: the correct file manager.
            """
            if mode == "xml":
                return XMLFilingParser(files)
            elif mode == "xhtml":
                return XHTMLFilingParser(files)
            else:
                # Make sure that only a supported mode is used
                raise ValueError("Mode must be 'xml' or 'xhtml'")

        # Make sure that only a supported mode is used
        if mode != "xml" and mode != "xhtml":
            raise ValueError("Mode must be 'xml' or 'xhtml'")

        # check if the path is a folder or a file
        is_uri = path.startswith("http")
        if not is_uri:
            path = os.path.abspath(path)

        is_file = os.path.isfile(path)
        is_dir = os.path.isdir(path)

        if DEBUG:  # pragma: no cover
            print(f"Path {path}, is file: {is_file}, is dir: {is_dir}, is uri: {is_uri}")

        if is_dir:
            if DEBUG:  # pragma: no cover
                print(f"Opening folder {path}")

            folder_filenames = os.listdir(path)
            files = list(filter(lambda x: search_filetypes(mode, x), folder_filenames))

            def prepend_path(filename: str) -> str:
                return os.path.join(path, filename)

            files = list(map(prepend_path, files))

            if len(files) == 0:
                raise ValueError(
                    f"No xml files found in folder {path}. Please provide a folder with at least one xml file."
                )

            parser = choose_file_manager(mode, files)
            return cls(parser)
        elif is_file and any(map(lambda x: search_filetypes(mode, x), [path, *args])):
            paths = [path, *args]
            if DEBUG:  # pragma: no cover
                print(f"Opening file {path}")
            files = list(filter(lambda x: search_filetypes(mode, x), paths))
            parser = choose_file_manager(mode, files)
            return cls(parser)
        elif is_file and path.endswith(".zip"):
            if DEBUG:  # pragma: no cover
                print(f"Opening zip file {path}")
            dir_path = os.path.dirname(path)
            print(f"Extracting {path} to {dir_path} and loading it")
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(dir_path)
                # get all file paths ending in xml
                files = list(filter(lambda x: search_filetypes(mode, x), zip_ref.namelist()))
            print(f"Finished extracting...")

            files = list(map(lambda x: os.path.join(dir_path, x), files))
            if len(files) == 0:
                raise ValueError(
                    f"No valid files found in zip file {path}. Please provide a zip file with at least one valid file."
                )
            else:
                return cls.open(files[0], mode, *files[1:])
        elif is_uri:
            if not search_filetypes(mode, path):
                raise NotImplementedError("Brel currently only supports XBRL filings in the form of XML files")

            if DEBUG:
                print(f"Opening uri {path}")
            # if the path is a uri, then download the file and place it in a folder
            # the folder is named after the last part of the uri without the extension

            # check if the uri points to an valid file
            if not search_filetypes(mode, path):
                raise ValueError(f"{path} is not a valid path")

            # open the file
            parser = choose_file_manager(mode, [path])
            return cls(parser)

        else:
            raise ValueError(f"{path} is not a valid path")

    def __init__(self, parser: IFilingParser) -> None:
        # check if the parser is the right type
        # otherwise, users might have called the constructor instead of the open method
        if not isinstance(parser, IFilingParser):
            raise ValueError(
                f"Use the `Filing.open(path)` method to open a filing. You called the constructor directly."
            )

        parser_result = parser.parse()

        self.__networks: list[INetwork] = parser_result["networks"]
        self.__facts: list[Fact] = parser_result["facts"]
        self.__reportelems: list[IReportElement] = parser_result["report elements"]
        self.__components: list[Component] = parser_result["components"]
        self.__nsmap = parser_result["nsmap"]
        self.__errors = parser_result["errors"]

    # first class citizens
    def get_all_facts(self) -> list[Fact]:
        """
        :return list[Fact]: a list of all [`Fact`](../facts/facts.md) objects in the filing.
        """
        return self.__facts

    def get_all_report_elements(self) -> list[IReportElement]:
        """
        :return list[IReportElement]: a list of all [`IReportElement`](../report-elements/report-elements.md) objects in the filing.
        """
        return self.__reportelems

    def get_all_components(self) -> list[Component]:
        """
        :return list[Component]: a list of all [`Component`](../components/components.md) objects in the filing.
        Note: components are sometimes called "roles" in the XBRL specification.
        """
        return self.__components

    def get_all_physical_networks(self) -> list[INetwork]:
        """
        Get all [`INetwork`](../components/networks.md) objects in the filing, where network.is_physical() is True.
        :return list[INetwork]: a list of all physical networks in the filing.
        """
        physical_networks = [network for network in self.__networks if network.is_physical()]
        return physical_networks

    def get_errors(self) -> list[Exception]:
        """
        :return list[Exception]: a list of all errors that occurred during parsing.
        """
        return self.__errors

    # second class citizens
    def get_all_concepts(self) -> list[Concept]:
        """
        :returns list[Concept]: a list of all concepts in the filing.
        Note that concepts are defined according to the Open Information Model. They are not the same as abstracts, line items, hypercubes, dimensions, or members.
        """
        return cast(
            list[Concept],
            list(filter(lambda x: isinstance(x, Concept), self.__reportelems)),
        )

    def get_all_abstracts(self) -> list[Abstract]:
        """
        :returns list[Abstract]: a list of all abstracts in the filing.
        """
        return cast(
            list[Abstract],
            list(filter(lambda x: isinstance(x, Abstract), self.__reportelems)),
        )

    def get_all_line_items(self) -> list[LineItems]:
        """
        :returns list[LineItems]: a list of all line items in the filing.
        """
        return cast(
            list[LineItems],
            list(filter(lambda x: isinstance(x, LineItems), self.__reportelems)),
        )

    def get_all_hypercubes(self) -> list[Hypercube]:
        """
        :returns list[Hypercube]: a list of all hypercubes in the filing.
        """
        return cast(
            list[Hypercube],
            list(filter(lambda x: isinstance(x, Hypercube), self.__reportelems)),
        )

    def get_all_dimensions(self) -> list[Dimension]:
        """
        :returns list[Dimension]: a list of all dimensions in the filing.
        """
        return cast(
            list[Dimension],
            list(filter(lambda x: isinstance(x, Dimension), self.__reportelems)),
        )

    def get_all_members(self) -> list[Member]:
        """
        :returns list[Member]: a list of all members in the filing.
        """
        return cast(
            list[Member],
            list(filter(lambda x: isinstance(x, Member), self.__reportelems)),
        )

    def get_report_element_by_name(self, element_qname: QName | str) -> IReportElement | None:
        """
        :param element_qname: the name of the report element to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns IReportElement|None: the report element with the given name. If no report element is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(element_qname, str):
            element_qname = QName.from_string(element_qname, self.__nsmap)

        def name_matches(x: IReportElement) -> TypeGuard[IReportElement]:
            return x.get_name() == element_qname

        re: IReportElement | None = next(filter(name_matches, self.__reportelems), None)

        return re

    def get_concept_by_name(self, concept_qname: QName | str) -> Concept | None:
        """
        :param concept_qname: the name of the concept to get. This can be a QName or a string in the format "prefix:localname". For example, "us-gaap:Assets".
        :returns Concept|None: the concept with the given name. If no concept is found, then None is returned.
        :raises ValueError: if the QName string is not a valid QName or if the prefix is not found.
        """
        if isinstance(concept_qname, str):
            concept_qname = QName.from_string(concept_qname, self.__nsmap)

        def concept_matches(x: IReportElement) -> TypeGuard[Concept]:
            return isinstance(x, Concept) and x.get_name() == concept_qname

        concept: Concept | None = next(filter(concept_matches, self.__reportelems), None)

        return concept

    def get_concept(self, concept_qname: QName | str) -> Concept | None:
        """
        Alias of `filing.get_concept_by_name(concept_qname)`.
        """
        return self.get_concept_by_name(concept_qname)

    def get_all_reported_concepts(self) -> list[Concept]:
        """
        Returns all concepts that have at least one fact reporting against them.
        :returns list[Concept]: The list of concepts
        """
        reported_concepts = []
        for fact in self.__facts:
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
            concept_name = QName.from_string(concept_name, self.__nsmap)

        filtered_facts = []
        for fact in self.__facts:
            concept = fact.get_concept().get_value()

            if concept.get_name() == concept_name:
                filtered_facts.append(fact)

        return filtered_facts

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
        return [component.get_URI() for component in self.__components]

    def get_component(self, uri: str) -> Component | None:
        """
        :param URI: the URI of the component to get.
        :return Component|None: the component with the given URI. None if no component is found.
        """
        for component in self.__components:
            if component.get_URI() == uri:
                return component
        return None

    def generate_fact_table_pandas_df(self) -> pd.DataFrame:
        """
        Converts the filing to a pandas DataFrame.
        :return pandas.DataFrame: the filing as a pandas DataFrame.
        """
        import pandas as pd

        data = []
        for fact in self.__facts:
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
        data = []
        for component in self.__components:
            d = component.convert_to_dict()
            data.append(d)

        df = pd.DataFrame(data)
        return df

    def get_all_labels(self) -> list[dict[str, str]]:
        """
        :return list[dict[str, str]]: a list of all labels in the filing.
        """
        labels = []
        for re in self.__reportelems:
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
        for re in self.__reportelems:
            d = re.convert_to_dict()
            data.append(d)

        df = pd.DataFrame(data)
        return df
