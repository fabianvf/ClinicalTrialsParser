import json
from glob import glob
from lxml import etree

from xml_to_json import xml_to_json

#TODO: Write test code.

class ClinicalTrialData(object):
    """Parses an XML file containing clinical trial study data from clinicaltrials.gov"""
    def __init__(self,file_name):
        """Upon init, reads XML file,and parses it for some key information.
		NOTE: Comment tags are included in the XML tree."""
        self.file_name = str(file_name)
        self.root = etree.parse(self.file_name).getroot()
        self.id = self.root.find('id_info').find('nct_id').text
        self.url = self.root.find('required_header').find('url').text
        self.raw = xml_to_json(self.file_name)
               
        self.current_status = self.root.find('overall_status').text
        self.phase = self.root.find('phase').text
        self.description = self.root.find('brief_summary')[0].text

        if self.root.find('official_title') == None:
			self.title = self.root.find('brief_title').text
        else:
			self.title = self.root.find('official_title').text

        self.contributors = []
        for entry in self.root.findall('overall_official'):
			official_dict = {}
			official_dict['full_name'] = entry.find('last_name').text
			official_dict['role'] = entry.find('role').text
			official_dict['affiliation'] = entry.find('affiliation').text
			official_dict['email'] = None
			self.contributors.append(official_dict)
		
        self.keywords = ["clinical trial"]
        for entry in self.root.findall('keyword'):
			self.keywords.append(entry.text)
        self.date_processed = self.__process_date()

        self.references = []
        for entry in self.root.findall('reference'):
			reference_dict = {'PMID':None}
			reference_dict['citation'] = entry.find('citation').text
			if entry.find('PMID') != None:
				reference_dict['PMID'] = entry.find('PMID').text
			self.references.append(reference_dict)
			
        self.locations = []		
        for entry in self.root.findall('location'):
			location_dict = {'location_name': None, 'location_zip': None}
			if entry.find('facility').find('name') != None:
				location_dict['location_name'] = entry.find('facility').find('name').text
			if entry.find('facility').find('address').find('zip') != None:
				location_dict['location_zip'] = entry.find('facility').find('address').find('zip').text
			self.locations.append(location_dict)

    def __process_date(self):
		"""Private method for parsing the xml for the date processed (by clinicaltrials.gov) info."""
		date_string = self.root.find('required_header').find('download_date').text
		date_string = date_string.replace('ClinicalTrials.gov processed this data on ', '')
		return date_string
    		
    def json_osf_format(self):
		"""Returns a dictionary that represents key information about the clinical trial in json format."""       
		json_osf = {
    		"imported_from": "clinicaltrials.gov",
    		"date_processed": self.date_processed,
    		"contributors": self.contributors,
    		"description": self.description,
    		"title": self.title,
    		"url": self.url,
    		"files":
            [('../ct_xml/' + str(self.id) + '.xml'), ('../ct_raw_json/' + str(self.id) + '_raw.json' )] +
            ['../{0}'.format(path) for path in glob('ct_archive/ct_changes/{0}/*'.format(str(self.id)))] + 
            ['../{0}'.format(path) for path in glob('ct_archive/ct_changes_xml/{0}/*'.format(str(self.id)))],
    		"tags": [
        		"clinicaltrials.gov"
    		],
            "versions": {path.rstrip('.json'):open(path).read() for path in glob('ct_archive/ct_changes_json/{0}/*'.format(self.id))}
		}
		json_osf['tags'] = json_osf['tags'] + self.keywords
		return json_osf

    def json_osf_to_txt(self):
		"""Writes the json returned by json_osf_format() to a text file."""
		with open((str(self.id) + '_osf.json'), 'w') as json_txt:
			json.dump(self.json_osf_format(), json_txt, sort_keys=True, indent=4)




