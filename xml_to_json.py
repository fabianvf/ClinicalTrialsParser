## converts RAW xml file to a RAW JSON file for archiving/importing purposes

from lxml import etree
import json
import xmltodict
import glob
from open_map_gps import get_coordinate
from clinical_trials_parser import ClinicalTrialData
def xml_to_json(xml_file, nct_id):

    tree = etree.parse(xml_file)
    ctd = ClinicalTrialData(xml_file)
    loc_list = ctd.locations
    xml_string = etree.tostring(tree)

    json_text = xmltodict.parse(xml_string)

    json_text['geocoordinates'] = get_coordinate(nct_id)
    
    json_text = json.dumps(json_text, sort_keys=True, indent=4)
    
    return json_text

def key_files_to_json():

    key_xml_folder = 'all_studies/'
    key_json_folder = 'all_raw_json/'

    xmlfiles = glob.glob(key_xml_folder + '*.xml')

    # get rid of the file extension
    xml_ids = [ext.replace('.xml','') for ext in xmlfiles]

    # get rid of the folder name
    xml_ids = [folder.replace(key_xml_folder,'') for folder in xml_ids]

    id_index = 0

    for filename in xmlfiles:
        json_text = xml_to_json(filename, xml_ids[id_index])

        with open(key_json_folder + xml_ids[id_index] +'_raw.json', "wb") as jt:
            jt.write(json_text)

        id_index += 1

# xml_to_json('ct_xml/NCT00000122.xml')

key_files_to_json()