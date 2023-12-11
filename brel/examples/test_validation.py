from lxml import etree
import requests
import time

import re

def get_version_from_url(url: str) -> str | None:

    version = ""
    sections = url.split("/")
    for section in sections:
        section = re.sub(r'[^0-9]', '', section)
        if section.isnumeric():
            version = section
    
    return version

def get_prefix_from_url(url: str):
    prefix = ""
    sections = url.split("/")
    for section in sections:
        section = re.sub(r'[^a-zA-Z]', '', section)
        section = section.replace("xsd", "")             

        if len(section) > 0 and "www" not in section:
            prefix = section
            
    return prefix

class OnlineResolver(etree.Resolver):
    def __init__(self) -> None:
        pass

    def resolve(self, system_url, public_id, context):
        # Resolve remote XSD files
        # Note: does not do any caching
        print("resolving", system_url)
        try:
            if system_url and system_url.startswith('http'):
                remote_xsd_content = requests.get(system_url, allow_redirects=True).content

                # extract the base url
                base_url = system_url.rsplit('/', 1)[0] + '/'

                return self.resolve_string(remote_xsd_content, context, base_url=base_url)
            else:
                # load the file from the local filesystem
                base_url = system_url.rsplit('/', 1)[0] + '/'
                file_prefix = get_prefix_from_url(system_url)
                file_version = get_version_from_url(system_url)
                file_name = f"{file_prefix}_{file_version}.xsd"
                file_path = base_url + file_name
                with open(file_path, "r") as xsd_file:
                    xsd_content = xsd_file.read()
                    return self.resolve_string(xsd_content, context, base_url=base_url)
                # print("not resolving", system_url)
        except Exception as e:
            print(f"Error resolving {system_url}: {e}")
            raise e


xsd_cache_path = "brel/dts_cache/"
# xsd_file = "usgaap_2023.xsd"
# xsd_file = "dei_2023.xsd"
xsd_file = "xbrlinstance_20031231.xsd"
xsd_file_path = xsd_cache_path + xsd_file
print("trying to parse xsd file: ", xsd_file)
start_time = time.time()

# create the resolver
print("creating resolver")
xsd_resolver = OnlineResolver()
xsd_parser = etree.XMLParser()
xsd_parser.resolvers.add(xsd_resolver)
print(f"DONE ({time.time() - start_time:.2f} sec)")

# parse the xsd file
print("parsing xsd file")
xsd_tree = etree.parse(xsd_file_path, parser=xsd_parser)
print(f"DONE ({time.time() - start_time:.2f} sec)")

# create the schema from the etree
print("creating schema")
schema = etree.XMLSchema(xsd_tree)
print(f"DONE ({time.time() - start_time:.2f} sec)")

