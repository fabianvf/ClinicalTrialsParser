## converts RAW xml file to a RAW JSON file for archiving/importing purposes

from lxml import etree
import json

def xml_to_json(xml_file):

    tree = etree.parse(xml_file)

    xml_string = etree.tostring(tree)

    json_txt = json.dumps(xml_string)

    return json_txt


xml_to_json('NCT01718405.xml')