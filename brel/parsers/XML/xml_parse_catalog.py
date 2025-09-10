from lxml.etree import _ElementTree, _Element
from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.parsers.utils.lxml_utils import get_str_attribute_optional

OASIS_NAMESPACE = "urn:oasis:names:tc:entity:xmlns:xml:catalog"


def parse_catalog_xml(
    catalog_filepath: str, catalog_tree: _ElementTree, filing_context: FilingContext
) -> None:
    uri_rewrite_repository = filing_context.get_uri_rewrite_repository()
    error_repository = filing_context.get_error_repository()

    root_node = catalog_tree.getroot()
    original_strings = set()
    catalog_filepath_pieces = catalog_filepath.split("/")

    if root_node.tag != f"{{{OASIS_NAMESPACE}}}catalog":
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.INVALID_CATALOG_ROOT_NODE, root_node
            )
        )

    for child in root_node.findall(
        "./er:rewriteURI", namespaces={"er": OASIS_NAMESPACE}
    ):
        original_string = child.get("uriStartString")
        replacement_string = child.get("rewritePrefix")

        if not original_string or not replacement_string:
            error_repository.upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.REWRITE_URI_MISSING_ATTRIBUTE, child
                )
            )

            continue

        if original_string in original_strings:
            error_repository.upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.MULTIPLE_REWRITE_URIS_FOR_START_STRING,
                    child,
                    uri=original_string,
                )
            )

        original_strings.add(original_string)

        replacement_string_pieces = replacement_string.split("/")

        complete_replacement_string = "/".join(
            catalog_filepath_pieces[:-1] + replacement_string_pieces
        )
        uri_rewrite_repository.upsert(original_string, complete_replacement_string)
