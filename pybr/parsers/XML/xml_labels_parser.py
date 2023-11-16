import lxml
import lxml.etree

from pybr import QName, PyBRLabel


def parse_labels_xml(
        xbrl_labels: lxml.etree._ElementTree
        ) -> dict[QName, list[PyBRLabel]]:
    """
    Parse the labels
    @return: A list of all the labels in the filing
    """

    labels: dict[QName, list[PyBRLabel]] = {}

    nsmap = QName.get_nsmap()

    # get all label xml elements
    # labels are xml elements with the tag link:label
    labels_xml = xbrl_labels.findall(".//link:label", namespaces=nsmap)

    for label_xml in labels_xml:
        label = PyBRLabel.from_xml(label_xml)

        # get the xlink:label attribute
        # this attribute contains the label id
        label_id = label_xml.get("{" + nsmap["xlink"] + "}label")

        # get the corresponding labelarc xml element
        # this element has the tag link:labelArc and the xlink:to attribute is the label id
        labelarc_xml = xbrl_labels.find(f".//link:labelArc[@xlink:to='{label_id}']", namespaces=nsmap)

        # get the locator id from the xlink:from attribute
        locator_id = labelarc_xml.get("{" + nsmap["xlink"] + "}from")

        # get the matching locator
        # the locator has the tag link:loc and the xlink:label attribute is the locator id
        locator_xml = xbrl_labels.find(f".//link:loc[@xlink:label='{locator_id}']", namespaces=nsmap)

        # the xlink:href attribute of the locator contains the report element name
        # split the href into an url and the filename
        _, report_element_name = locator_xml.get("{" + nsmap["xlink"] + "}href").split("#")

        # turn the report element name into a QName
        # TODO: improve the segment that alters the report_element_name into a valid qname
        # this is a temporary fix
        # replace the last "_" with ":"
        report_element_name = report_element_name.rsplit("_", 1)[0] + ":" + report_element_name.rsplit("_", 1)[1]

        report_element_qname = QName.from_string(report_element_name)

        re_labels = labels.get(report_element_qname, [])
        re_labels.append(label)
        labels[report_element_qname] = re_labels


    return labels