from lxml import etree
import requests
import os

class OnlineResolver(etree.Resolver):
    def __init__(self) -> None:
        pass

    def resolve(self, system_url, public_id, context):
        # Resolve remote XSD files
        # print("resolving", system_url)
        try:
            if system_url and system_url.startswith('http'):
                remote_xsd_content = requests.get(system_url, allow_redirects=True).content

                # extract the base url
                base_url = system_url.rsplit('/', 1)[0] + '/'

                return self.resolve_string(remote_xsd_content, context, base_url=base_url)
        except Exception as e:
            print(f"Error resolving {system_url}: {e}")
            raise e


xsd_cache_path = "brel/dts_cache/"
all_files = os.listdir(xsd_cache_path)
xsd_files = [f for f in all_files if f.endswith(".xsd")]
xsd_files.reverse()

print("xsd_files", xsd_files)

xsd_file = "ko-20230630.xsd"
# xsd_file = "https__xbrl.sec.gov_ecd_2023_ecd-2023.xsd"

xsd_file_path = xsd_cache_path + xsd_file
print("trying to parse xsd file: ", xsd_file)


xsd_resolver = OnlineResolver()
xsd_parser = etree.XMLParser()
xsd_parser.resolvers.add(xsd_resolver)

xsd_tree = etree.parse(xsd_file_path, parser=xsd_parser)

print("tree parsed")

# find all elements in the us-gaap namespace. the tag of the element does not matter
# us_gaap_elements = xsd_tree.findall(".//{http://fasb.org/us-gaap/2023}LiabilityForCatastropheClaimsCarryingAmount")
us_gaap_elements = xsd_tree.findall(".//")

print("us_gaap_elements", us_gaap_elements)

# print(etree.tostring(xsd_tree, pretty_print=True))

schema = etree.XMLSchema(xsd_tree)

