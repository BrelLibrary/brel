"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 2 May 2025

====================
"""

from brel.data.namespace.namespace_repository import NamespaceRepository
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.qnames.qname import QName
from brel.qnames.qname_search_params import QNameSearchParams
from brel.reportelements.i_report_element import IReportElement


class ReportElementService:
    def __init__(
        self,
        namespace_repository: NamespaceRepository,
        report_element_repository: ReportElementRepository,
    ) -> None:
        self.__namespace_repository = namespace_repository
        self.__report_element_repository = report_element_repository

    def get_fuzzy_typed[
        T: IReportElement
    ](self, search_params: QNameSearchParams, report_element_type: type[T],) -> list[T]:
        uri_candidates: set[str] = set()
        if search_params.uri:
            uri_candidates.add(search_params.uri)

        prefix_candidates: set[str] = set()
        if search_params.prefix:
            prefix_candidates.add(search_params.prefix)

        if search_params.uri and not search_params.prefix:
            prefix_candidates = set(
                self.__namespace_repository.get_prefixes(search_params.uri)
            )
        elif not search_params.uri and search_params.prefix:
            uri_candidates = set(
                self.__namespace_repository.get_uris(search_params.prefix)
            )

        if uri_candidates or prefix_candidates:
            qname_candidates = (
                QName(
                    uri,
                    prefix,
                    search_params.local_name,
                )
                for uri in uri_candidates
                for prefix in prefix_candidates
            )

            matching_qnames = filter(
                lambda qname: self.__report_element_repository.has_typed_qname(
                    qname, report_element_type
                ),
                qname_candidates,
            )

            return [
                self.__report_element_repository.get_typed_by_qname(
                    qname, report_element_type
                )
                for qname in matching_qnames
            ]
        else:
            return list(
                filter(
                    lambda qname: qname.get_name().local_name
                    == search_params.local_name,
                    self.__report_element_repository.get_all_typed(report_element_type),
                )
            )

    def get_fuzzy(self, search_params: QNameSearchParams) -> list[IReportElement]:
        # TODO schmidi replace with call to find_typed and make typechecker happy somehow
        uri_candidates: set[str] = set()
        if search_params.uri:
            uri_candidates.add(search_params.uri)

        prefix_candidates: set[str] = set()
        if search_params.prefix:
            prefix_candidates.add(search_params.prefix)

        if search_params.uri and not search_params.prefix:
            prefix_candidates = set(
                self.__namespace_repository.get_prefixes(search_params.uri)
            )
        elif not search_params.uri and search_params.prefix:
            uri_candidates = set(
                self.__namespace_repository.get_uris(search_params.prefix)
            )

        if uri_candidates or prefix_candidates:
            return list(
                map(
                    self.__report_element_repository.get_by_qname,
                    filter(
                        lambda qname: self.__report_element_repository.has_qname(qname),
                        [
                            QName(
                                uri,
                                prefix,
                                search_params.local_name,
                            )
                            for uri in uri_candidates
                            for prefix in prefix_candidates
                        ],
                    ),
                )
            )
        else:
            return list(
                filter(
                    lambda qname: qname.get_name().local_name
                    == search_params.local_name,
                    self.__report_element_repository.get_all(),
                )
            )
