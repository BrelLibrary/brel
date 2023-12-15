from brel import Filing
from brel.networks import ReferenceNetwork, CalculationNetwork
from brel.utils import pprint_network

import lxml
import lxml.etree
import os
import requests
from brel.parsers.dts import XMLFileManager


class SchemaResolver(lxml.etree.Resolver):
    def __init__(self, parser) -> None:
        self.cache_location = "brel/dts_cache/"
    
    def url_to_filename(self, url: str) -> str:
        """
        Convert a url to a filename.
        @param url: The url to convert.
        @return: The filename.
        """
        result = url.split("/")[-2:]
        result_str = "_".join(result)
        return result_str
    
    def resolve(self, system_url: str = "", public_id: str = "", context=None):
        # print (f"Resolving {system_url}")
        # if system_url.startswith("http"):
        #     response = requests.get(system_url)
        #     print(response.status_code)
        #     try:
        #         result = super().resolve_string(response.text, context, base_url=system_url)
        #         print(result)
        #         return result
        #     except Exception as e:
        #         print(e)
        #         raise e
        # else:
        #     print("fallback to default resolver")
        #     return super().resolve(system_url, public_id, context)

        if system_url.endswith(".xsd"):
            filepath = self.cache_location + self.url_to_filename(system_url)
            print(f"Filepath: {filepath}")
            print(f"system_url: {system_url}")
            return self.resolve_file(open(filepath, "rb"), context, base_url=system_url, close=True)
        else:
            # return super().resolve(system_url, public_id, context)
            print("asdfasdf")
            raise ValueError(f"system_url: {system_url} is not a valid schema url")





def example6():
    # print the files in the reports/coca_cola directory
    # print(os.listdir("reports/coca_cola/"))

    # # try to parse ../dts_cache/2023-ecd-2023.xsd with lxml
    # some_xml = lxml.etree.parse("reports/coca_cola/ko-20230630_htm.xml")

    # schema_tree = lxml.etree.parse("brel/dts_cache/ko-20230630.xsd")
    # schema_tree = lxml.etree.parse("brel/dts_cache/us-types-2023.xsd")
    # schema_tree = lxml.etree.parse("brel/dts_cache/2003_xbrl-instance-2003-12-31.xsd")
    # schema = lxml.etree.XMLSchema(schema_tree)

    parser = lxml.etree.XMLParser()

    parser.resolvers.add(SchemaResolver(parser))

    
    schema_tree = lxml.etree.parse("brel/dts_cache/2020-01-21_types.xsd")
    # schema = lxml.etree.XMLSchema(schema_tree)

    # schema_tree = lxml.etree.parse("ko-20230630.xsd", parser)
    schema = lxml.etree.XMLSchema(schema_tree)


    print(schema)


    # filing = Filing.open("reports/coca_cola/")

    # networks = filing.get_all_pyhsical_networks()

    # for network in networks:
    #     # if isinstance(network, ReferenceNetwork):
    #         # pprint_network(network)
    #     # pprint_network(network)
    #     if isinstance(network, CalculationNetwork):
    #         pprint_network(network)