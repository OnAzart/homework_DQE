import argparse
import xml.etree.ElementTree as ET

def parse_and_remove(filename, path):
   path_parts = path.split('/')
   doc = ET.iterparse(filename, ('start', 'end'))
   # Skip root element
   next(doc)
   tag_stack = []
   elem_stack = []
   for event, elem in doc:
    if event == 'start':
      tag_stack.append(elem.tag)
      elem_stack.append(elem)
    elif event == 'end':
                if tag_stack == path_parts:
                    yield elem
                try:
                    tag_stack.pop()
                    elem_stack.pop()
                except IndexError:
                    pass


parser_args = argparse.ArgumentParser(description="function of XML parsing. Just distinct government")
parser_args.add_argument('-xml', '-path', help='Path to XML')
args = parser_args.parse_args()
path = args.xml

if not path:
    path = "D://DQE//mondial-3.0.xml"

government_types = []
countries = parse_and_remove(path, 'country')
for country in countries:
    name = country.attrib['name']
    government = country.attrib['government']
    government_types.append(government.strip())

distinct_government_types = set(government_types)
for government in distinct_government_types:
    print(f"{government},", end=' ')
print('\b\b')
