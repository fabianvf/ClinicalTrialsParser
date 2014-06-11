## converts RAW xml file to a RAW JSON file for archiving/importing purposes

from lxml import etree
import json
import xmltodict
import glob

def xml_to_json(xml_file):

    tree = etree.parse(xml_file)
    xml_string = etree.tostring(tree)

    json_text = xmltodict.parse(xml_string)

    json_text = json.dumps(json_text, sort_keys=True, indent=4)

    return json_text

def key_files_to_json():

    key_xml_folder = 'ct_xml/'
    key_json_folder = 'ct_raw_json/'

    xmlfiles = glob.glob(key_xml_folder + '*.xml')

    # get rid of the file extension
    xml_ids = [ext.replace('.xml','') for ext in xmlfiles]

    # get rid of the folder name
    xml_ids = [folder.replace('ct_xml/','') for folder in xml_ids]

    id_index = 0

    for filename in xmlfiles:
        json_text = xml_to_json(filename)

        with open(key_json_folder + xml_ids[id_index] +'_raw.json', "wb") as jt:
            jt.write(json_text)

        id_index += 1

# xml_to_json('NCT02152930.xml')

key_files_to_json()
