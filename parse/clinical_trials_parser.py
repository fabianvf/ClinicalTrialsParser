from glob import glob
from lxml import etree
import xmltodict
import time

from location_to_coordinates import LocationToCoord as l2c

def get_locations(root):
    locations = []
    for entry in root.findall('location'):
        location_dict = {'name': None, 'zip': None, 'city': None, 'state': None, 'country': None}
        if entry.find('facility').find('name') != None:
            location_dict['name'] = entry.find('facility').find('name').text
        if entry.find('facility').find('address').find('zip') != None:
            location_dict['zip'] = entry.find('facility').find('address').find('zip').text
        if entry.find('facility').find('address').find('city') != None:
            location_dict['city'] = entry.find('facility').find('address').find('city').text
        if entry.find('facility').find('address').find('country') != None:
            location_dict['country'] = entry.find('facility').find('address').find('country').text
        if entry.find('facility').find('address').find('state') != None:
            location_dict['state'] = entry.find('facility').find('address').find('state').text
        locations.append(location_dict)
    return locations

 
def parse(file_name):
    trial = {}

    root = etree.parse(file_name).getroot()
    trial['id'] = root.find('id_info').find('nct_id').text
    trial['phase'] = root.find('phase').text
    trial['description'] = root.find('brief_summary')[0].text
   
    if root.find('official_title') == None:
        trial['title'] = root.find('brief_title').text
    else:
        trial['title'] = root.find('official_title').text

    trial['contributors'] = []
    for entry in root.findall('overall_official'):
        official_dict = {}
        official_dict['full_name'] = entry.find('last_name').text
        official_dict['role'] = entry.find('role').text
        official_dict['affiliation'] = entry.find('affiliation').text
        official_dict['email'] = None
        trial['contributors'].append(official_dict)

    trial['keywords'] = ["clinical trial"]
    for entry in root.findall('keyword'):
        trial['keywords'].append(entry.text)

    date_string = root.find('required_header').find('download_date').text
    trial['date_processed'] = date_string.replace('ClinicalTrials.gov processed this data on ', '')

    trial['locations'] = get_locations(root)
    return trial
    

def xml_to_json(xml_file):
    tree = etree.parse(xml_file)
    xml_string = etree.tostring(tree)
    blob = xmltodict.parse(xml_string)
    locations = get_locations(tree.getroot())
    blob['geodata'] = l2c(locations)
    return blob

def json_osf_format(nct_id):
    files = set([f.rstrip('-before').rstrip('-after') for f in glob('files/{0}/*.xml'.format(nct_id))])
    files = sorted(files, key=lambda v: time.mktime(time.strptime(v.split('/')[-1].rstrip('.xml').rstrip('-before').rstrip('-after').split('_')[-1], '%m%d%Y')))

    if len(files) == 0:
        return None
    versions = {'original': xml_to_json(files[0])}
    for f in files:
        if 'after' in f:
            version = f.split('/')[-1].rstrip('.xml').rstrip('-after').split('_')[-1]
            versions[version] = xml_to_json(f)
            
    trial = parse('xml/{0}.xml'.format(nct_id))

    json_osf = {
        "imported_from": "clinicaltrials.gov",
        "date_processed": trial['date_processed'],
        "contributors": trial['contributors'],
        "description": trial['description'],
        "id": trial['id'],
        "title": trial['title'],
        "files": glob('files/{0}/*'.format(str(trial['id']))),
        "tags": [
            "clinical trial"
        ],
        "versions": versions,
        "phase": trial['phase'],
        "geo_data": trial['locations'],
        "keywords": trial['keywords']
    }
    return json_osf

