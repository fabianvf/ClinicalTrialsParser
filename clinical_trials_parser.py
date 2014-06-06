import requests
import json
from lxml import etree

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
		self.title = self.root.find('official_title').text
		self.description = self.root.find('brief_summary')[0].text
		self.contributors = []
		for entry in self.root.findall('overall_official'):
			official_dict = {}
			official_dict['full_name'] = entry.find('last_name').text
			official_dict['role'] = entry.find('role').text
			official_dict['affiliation'] = entry.find('affiliation').text
			self.contributors.append(official_dict)
		self.keywords = ["clinical trial"]
		for entry in self.root.findall('keyword'):
			self.keywords.append(entry.text)
		self.current_status = self.root.find('overall_status').text
		self.phase = self.root.find('phase').text
		self.date_processed = self.__process_date()
		self.references = []
		for entry in self.root.findall('reference'):
			reference_dict = {}
			reference_dict['citation'] = entry.find('citation').text
			reference_dict['PMID'] = entry.find('PMID').text
			self.references.append(reference_dict)
		self.locations = []
		for entry in self.root.findall('location'):
			location_tuple = ((entry.find('facility').find('name').text), (entry.find('facility').find('address').find('zip').text))
			self.locations.append(location_tuple)
	def __process_date(self):
		date_string = self.root.find('required_header').find('download_date').text
		date_string = date_string.replace('ClinicalTrials.gov processed this data on ', '')
		return date_string
	def json_osf_format(self):
		"""Returns a dictionary that represents key information about the clinical trial in json format."""
		json_osf = {
    		"imported_from": "clinicaltrials.gov",
    		"date_processed": self.date_processed,
    		"contributors": None,
    		"description": None,
    		"id": self.id,
    		"title": None,
    		"url": None,
    		"files": str(self.id) + '.xml',
    		"tags": [
        		"clinical trial"
    		],
    		"phase": None,
    		"current_status": None,
    		"geo_data": None,
    		"references": None,
    		"components": [{"title":"MetaData","description":None}]
		}
		json_osf['contributors'] = self.contributors
		json_osf['title'] = self.title
		json_osf['description'] = self.description
		json_osf['id'] = self.id
		json_osf['url'] = self.url
		json_osf['tags'] = self.keywords
		json_osf['phase'] = self.phase
		json_osf['current_status'] = self.current_status
		json_osf['geo_data'] = self.locations
		json_osf['references'] = self.references
		return json_osf

	def json_osf_to_txt(self):
		with open((str(self.id) + '_osf.json'), 'w') as json_txt:
			json.dump(self.json_osf_format(), json_txt, sort_keys=True, indent=4)

x = ClinicalTrialData('NCT00001372.xml')
print x.json_osf_to_txt()