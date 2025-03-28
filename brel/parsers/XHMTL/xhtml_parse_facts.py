from typing import cast, Mapping, Iterable, Tuple
import lxml.etree, re
from brel import Context, Fact, QName, QNameNSMap
from brel.characteristics import *
from brel.parsers.XML import parse_context_xml
from brel.parsers.XML.characteristics import parse_unit_from_xml
from brel.reportelements import Concept, IReportElement


def parse_fact_from_ixbrl(
    continuations: list[lxml.etree._Element],
    fact_xml_element: lxml.etree._Element,
    context: Context,
) -> Fact:
    """
    Create a single Fact from an lxml.etree._Element.
    :param continuations: The list of all the continuation facts
    :param fact_xml_element: The lxml.etree._Element to create the Fact from.
    :param context: The context of the fact. Note that new characteristics will be added to the context.
    :returns: The newly created Fact.
    """

    fact_id = fact_xml_element.get("id")
    fact_concept_name = fact_xml_element.get("name")
    fact_value = fact_xml_element.text

    if fact_value is None:
        fact_value = re.sub(r"\s+", " ", " ".join(fact_xml_element.itertext()))

        concept = context.get_concept().get_value()
        if not concept.is_nillable():
            raise ValueError(f"Fact {fact_id} has no value but the concept {concept.get_name()} is not nillable")

        if fact_value is None:
            fact_value = ""

    fact_context_ref = fact_xml_element.get("contextRef", default=None)
    fact_unit_ref = fact_xml_element.get("unitRef", default=None)

    # check if the fact has the correct context
    if fact_context_ref != context._get_id():
        raise ValueError(f"Fact {fact_id} has context {fact_context_ref} but should have context {context._get_id()}")

    # check if the fact has the correct unit
    # Note that the unit_ref is only the local name of the unit whilst the context_unit is the full QName.
    context_unit: UnitCharacteristic = cast(UnitCharacteristic, context.get_characteristic(Aspect.UNIT))
    if context_unit and fact_unit_ref and context_unit and fact_unit_ref != context_unit.get_value():
        raise ValueError(f"Fact {fact_id} has unit {fact_unit_ref} but should have unit {context_unit.get_value()}")

    # check if the fact has the correct concept
    context_concept: ConceptCharacteristic = cast(ConceptCharacteristic, context.get_characteristic(Aspect.CONCEPT))
    if fact_concept_name != context_concept.get_value().get_name().get():
        raise ValueError(
            f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_value().get_name().get()}"
        )

    # Check the format and apply the necessary formatting
    if (
        fact_xml_element.tag == "ix:nonFraction"
        or fact_xml_element.tag == "{http://www.xbrl.org/2013/inlineXBRL}nonFraction"
    ):
        fact_format = fact_xml_element.get("format")
        fact_scale = fact_xml_element.get("scale")
        if fact_format == "ixt:fixed-empty":
            fact_value = ""
        elif fact_format == "ixt:fixed-false":
            fact_value = "false"
        elif fact_format == "ixt:fixed-true":
            fact_value = "true"
        elif fact_format == "ixt:fixed-zero":
            fact_value = "0"
        elif fact_format == "ixt:num-dot-decimal":
            fact_value = fact_value.replace(",", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace(".", "").replace(" ", "").replace(",", ".")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace(",", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-dot-decimal-apos":
            fact_value = fact_value.replace("'", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace("'", "").replace(" ", "").replace(",", ".")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace("'", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        else:
            raise ValueError(f"Fact format {fact_format} not yet supported by XBRL")

    # Aggregate the continuation facts
    try:
        if fact_xml_element.get("continuedAt"):
            cont = list(
                filter(
                    lambda x: x.get("id") == fact_xml_element.get("continuedAt"),
                    continuations,
                )
            )[0]
            fact_value += cont.text
    except:
        fact_value

    return Fact(context, fact_value, fact_id)


def parse_facts_xhtml(
    etrees: Iterable[lxml.etree._ElementTree],
    report_elements: Mapping[QName, IReportElement],
    qname_nsmap: QNameNSMap,
) -> Tuple[list[Fact], dict[str, Fact], list[Exception]]:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    :param report_elements: The report elements
    :param qname_nsmap: The qname to namespace map
    :returns:
    - list[Fact]: The parsed facts
    - dict[str, Fact]: The id to fact mapping
    - list[Exception]: The exceptions that occurred during parsing
    """

    # Since many facts share the same characteristics, we cache the characteristics and reuse them.
    # instead of passing the cache around, we use these functions to get and add characteristics to the cache
    characteristics_cache: dict[str, ICharacteristic | Aspect] = {}

    def get_from_cache(key: str) -> ICharacteristic | Aspect | None:
        if key in characteristics_cache:
            return characteristics_cache[key]
        else:
            return None

    def add_to_cache(key: str, characteristic: ICharacteristic | Aspect) -> None:
        characteristics_cache[key] = characteristic

    # the same is true for report elements and qnames. Instead of passing dicts and nsmaps around, we use these functions
    def make_qname(qname_str: str) -> QName:
        return QName.from_string(qname_str, qname_nsmap)

    def get_report_element(qname: QName) -> IReportElement | None:
        if qname in report_elements:
            return report_elements[qname]
        else:
            return None

    # Next, we parse the facts
    facts: list[Fact] = []
    # in XBRL, some locators in networks can point to facts
    # Example: <locators href="http://www.example.com/my_schema.xsd#1234" label="some_label"/>
    # In this case, the locator points to an xml element in file my_schema.xsd with the attribute id="1234"
    # This xml element can be many things. A fact, a report element, ...
    # So we need to have a mapping from id -> fact to be able to resolve these locators
    id_to_fact: dict[str, Fact] = {}

    errors: list[Exception] = []

    for xbrl_instance in etrees:
        # get all xml elements in the instance that have a contextRef attribute
        ix_facts = xbrl_instance.xpath(
            ".//ix:nonNumeric | .//ix:nonFraction | .//ix:fraction",  # ix:continuation - add it to something, ix:exclude - remove all things in there
            namespaces={"ix": "http://www.xbrl.org/2013/inlineXBRL"},
        )  # Throw error saying that the OIM forbids fractions. ix:hidden

        continuations = xbrl_instance.xpath(
            ".//ix:continuation",  # ix:continuation - add it to something, ix:exclude - remove all things in there
            namespaces={"ix": "http://www.xbrl.org/2013/inlineXBRL"},
        )

        for ix_fact in ix_facts:
            # get the unit and concept characteristics
            # Not all of the characteristics of a context are part of the "syntactic context" xml element
            # These characteristics need to be searched for in the xbrl instance, parsed separately and added to the context
            # These characteristics are the concept (mandatory) and the unit (optional)
            characteristics: list[UnitCharacteristic | ConceptCharacteristic] = []

            fact_id = ix_fact.get("id")

            # ======== PARSE THE CONCEPT ========
            # get the concept name
            concept_name = ix_fact.get("name")
            if concept_name is None:
                print(f"Concept name error: name is None. Please report this error to team.")
                errors.append(ValueError(f"Fact with id {fact_id} has no tag"))
                continue

            # check cache for concept
            concept_characteristic = get_from_cache(f"concept {concept_name}")
            if concept_characteristic is None:
                # if the concept is not in the cache, create it
                concept_qname = make_qname(concept_name)
                concept = get_report_element(concept_qname)
                if concept is None:
                    print(f"Concept None error: Concept is None.  Please report this error to team.")
                    errors.append(ValueError(f"Concept {concept_qname} not found in report elements"))
                    continue

                if not isinstance(concept, Concept):
                    print(f"Concept instance error: not an instance of Concept. Please report this error to team.")
                    errors.append(ValueError(f"Concept {concept_qname} is not a concept. It is a {type(concept)}"))
                    continue

                concept_characteristic = ConceptCharacteristic(concept)
                add_to_cache(f"concept {concept_name}", concept_characteristic)
            else:
                # if the concept is in the cache, type check it
                if not isinstance(concept_characteristic, ConceptCharacteristic):
                    print(
                        f"ConceptCharacteristic error: not an instance of ConceptCharacteristic. Please report this error to team."
                    )
                    errors.append(
                        ValueError(f"Concept {concept_name} is not a concept. It is a {type(concept_characteristic)}")
                    )
                    continue

                concept_characteristic = cast(ConceptCharacteristic, concept_characteristic)
                concept = concept_characteristic.get_value()

            # add the concept to the characteristic list
            characteristics.append(concept_characteristic)

            # ======== PARSE THE UNIT ========
            # if there is a unit id, then find the unit xml/xhtml element, parse it and add it to the characteristics list
            # get the unit id
            unit_id = ix_fact.get("unitRef")

            if unit_id:
                # check cache for unit
                unit_characteristic = get_from_cache(unit_id)
                if unit_characteristic is None:
                    # create the unit if it is not in the cache
                    # print(f"{{*}}unit[@id='{unit_id}']")
                    # unit_xml = xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']")
                    unit_xml = xbrl_instance.xpath(
                        ".//xbrli:unit",
                        namespaces={"xbrli": "http://www.xbrl.org/2003/instance"},
                    )[0]
                    if unit_xml is None:
                        raise ValueError(f"Unit {unit_id} not found in xbrl instance")

                    try:
                        unit_characteristic = parse_unit_from_xml(
                            unit_xml,
                            concept,
                            make_qname,
                            get_from_cache,
                            add_to_cache,
                        )
                        add_to_cache(unit_id, unit_characteristic)
                    except Exception as e:
                        print(f"Unit error {e}")
                        errors.append(e)
                        continue

                else:
                    # if the unit is in the cache, type check it
                    if not isinstance(unit_characteristic, UnitCharacteristic):
                        print(
                            f"UnitCharacteristic error: not an instance of UnitCharacteristic. Please report this error to team."
                        )
                        errors.append(ValueError(f"Unit {unit_id} is not a unit. It is a {type(unit_characteristic)}"))
                        continue

                characteristics.append(unit_characteristic)

            # ======== PARSE THE CONTEXT ========
            # Note that there is a 1:1 mapping between facts and contexts. Therefore, if we cache facts, the contexts are cached as well.
            # First get the context id
            # This attribute is mandatory according to the XBRL specification
            context_id = ix_fact.get("contextRef")
            if context_id is None:
                print(f"Context ID error: contextRef is None. Please report this error to team.")
                errors.append(ValueError(f"Fact with id {fact_id} has no contextRef attribute"))
                continue

            # the context xml element has the tag context and the id is the context_id
            # xml_context = xbrl_instance.find(f"{{*}}context[@id='{context_id}']", namespaces=None)
            context = xbrl_instance.xpath(
                ".//xbrli:context",
                namespaces={"xbrli": "http://www.xbrl.org/2003/instance"},
            )
            xml_context = list(filter(lambda x: x.get("id") == context_id, context))[0]
            if xml_context is None:
                print(f"Context error: Context not found. Please report this error to team.")
                errors.append(ValueError(f"Context {context_id} not found in xbrl instance"))
                continue

            # then parse the context
            try:
                context = parse_context_xml(
                    xml_context,
                    characteristics,
                    make_qname,
                    get_report_element,
                    get_from_cache,
                    add_to_cache,
                )
            except Exception as e:
                print(f"Context parsing error {e}")
                errors.append(e)
                continue

            # create the fact
            try:
                fact = parse_fact_from_ixbrl(continuations, ix_fact, context)

                facts.append(fact)

                # add the fact to the id_to_fact mapping if it has an id
                if fact_id:
                    id_to_fact[fact_id] = fact
            except Exception as e:
                print(f"Fact read error {e}")
                errors.append(e)

    return facts, id_to_fact, errors
