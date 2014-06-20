from glob import glob
from lxml import etree
import xmltodict
import time
import json
from Bio import Entrez
from Bio import Medline
from bs4 import BeautifulSoup
import requests

from location_to_coordinates import LocationToCoord as l2c

#TODO: Should we remove the phase and locations finding code from the parse function? That information should be version specific? I already
#removed the phase and location entries from the json that's produced by the json_osf_format() function.

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
    return blob, locations

def scrape_pubmed_info(pmid):
    BASE = 'http://www.ncbi.nlm.nih.gov/pubmed/'
    pmid_info = {}

    html = requests.get(BASE + pmid)
    soup = BeautifulSoup(html.text)

    abstract_div = soup.find("div", {"class": "rprt abstract"})

    pmid_info['title'] = abstract_div.find("h1").text
    pmid_info['authors'] = abstract_div.find("div", {"class":"auths"}).text
    pmid_info['abstract'] =  abstract_div.find("div", {"class":"abstr"}).text
    pmid_info['link'] = BASE + pmid

    return pmid_info

def get_pubmed_info(pmid):
    pmid_info = {}
    BASE = 'http://www.ncbi.nlm.nih.gov/pubmed/'
    Entrez.email = 'pjfan@live.unc.edu'
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        pmid_info['title'] = record.get("TI", "?")
        pmid_info['authors'] = record.get("AU", "?")
        pmid_info['abstract'] =  record.get("AB", "?")
        pmid_info['link'] = BASE + pmid

    return pmid_info

def add_pubmed_to_references(nct_json):

    refs = None
    bg = nct_json.get('clinical_study').get('background')
    if bg: 
        refs = bg.get('reference')
    if refs:
        if not isinstance(refs, list):
            refs = [refs]
        for element in refs:
            reference = {}
            reference['citation'] = element.get('citation')
            reference['PMID'] = element.get('PMID')
            if reference['PMID']:
                reference['info']  = get_pubmed_info(reference['PMID'])
            references.append(reference)

    return references

def json_osf_format(nct_id):
    files = set([f.rstrip('-before').rstrip('-after') for f in glob('files/{0}/*.xml'.format(nct_id))])
    files = sorted(files, key=lambda v: time.mktime(time.strptime(v.split('/')[-1].rstrip('.xml').rstrip('-before').rstrip('-after').split('_')[-1], '%Y%m%d')))

    if len(files) == 0:
        return None
    
    trial = parse('xml/{0}.xml'.format(nct_id))

    versions = {}
    for f in files:
        version = f.split('/')[-1].rstrip('.xml').rstrip('-after').split('_')[-1]
        v, locations = xml_to_json(f)
        v['geo_data'] = l2c(locations)
        v['references'] = add_pubmed_to_references(v)
        versions[version] = v

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
        "keywords": trial['keywords']
    }
    
    return json_osf

with open('test_json','w') as json_text:
    json.dump(json_osf_format('NCT00000122'), json_text, indent=4, sort_keys=True)


print get_pubmed_info('90086934')
