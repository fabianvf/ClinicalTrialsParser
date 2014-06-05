import requests
import json
import time
import datetime
from lxml import etree

#TODO: Agree on a naming system for json/xml files, and the json for OSF import?
#TODO: Do we need to change or remove the time-stamp? It's generated when the instance of the object is created which is no longer the same time as when the data is retrieved from the server.
#TODO: Write test code.
#TODO: Extract location data and citation/reference data.

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
		self.time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

	def json_osf_format(self):
		"""Returns a dictionary that represents key information about the clinical trial in json format."""
		json_osf = {
    		"source": "clinicaltrials.gov",
    		"time_retrieved": self.time_stamp,
    		"contributors": None,
    		"description": None,
    		"id": self.id,
    		"title": None,
    		"url": None,
    		"tags": [
        		"clinical trial"
    		],
    		"phase": None,
    		"current_status": None,
		}
		json_osf['contributors'] = self.contributors
		json_osf['title'] = self.title
		json_osf['description'] = self.description
		json_osf['id'] = self.id
		json_osf['url'] = self.url
		json_osf['tags'] = self.keywords
		json_osf['phase'] = self.phase
		json_osf['current_status'] = self.current_status
		return json_osf

	def json_osf_to_txt(self):
		with open(('CTgov_study_' + str(self.id) + '.json'), 'w') as json_txt:
			json.dump(self.json_osf_format(), json_txt, sort_keys=True, indent=4)

