import requests
import json
import time
import datetime



class ClinicalTrialData(object):
	"""Uses the Lilly COI API to GET clinical trial study data in the form of Json."""
	def __init__(self,id):
		"""Upon init, sends get request to Lilly API, gets json in return and parses it for info."""
		self.id = id
		self.url = 'http://api.lillycoi.com/v1/trials/' + id + '.json'
		self.request = requests.get(self.url)
		self.json = self.request.json()
		self.title = self.json['results'][0]['official_title']
		self.description = self.json['results'][0]['brief_summary']['textblock']
		self.contributors = self.__populate_contributors()
		self.keywords = ["clinical trial"]
		for keyword in self.json['results'][0]['keyword']:
			self.keywords.append(keyword)
		self.time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		if self.json['results'][0]['condition_browse'] != {}:
			for term in self.json['results'][0]['condition_browse']['mesh_term']:
				self.keywords.append(term)
		if self.json['results'][0]['intervention_browse'] != {}:
			for term in self.json['results'][0]['intervention_browse']['mesh_term']:
				self.keywords.append(term)
	def json_to_txt(self):
		"""Saves the clinical trial json returned by the Lilly API as a text file."""
		with open((self.id + '.json'), 'w') as json_txt:
			json.dump(self.json, json_txt, sort_keys=True, indent=4)

	def __populate_contributors(self):
		"""Private method for parsing through returned json and making a list of contributors."""
		contributors = []
		for entry in self.json['results'][0]['overall_official']:
			contr_dict = {}	
			if entry['first_name'] == None:
				contr_dict['full_name'] = entry['last_name']
			else:
				contr_dict['full_name'] = entry['first_name'] + entry['last_name']
			contr_dict['role'] = entry['role']
			contributors.append(contr_dict)
		return contributors

	def json_osf_format(self):
		"""Returns a dictionary that represents key information about the clinical trial in json format."""
		json_osf = {
    		"source": "lilly",
    		"time_retrieved": self.time_stamp,
    		"title": None,
    		"contributors": None,
    		"description": None,
    		"id": self.id,
    		"title": None,
    		"url": None,
    		"tags": [
        		"clinical trial"
    		]
		}
		json_osf['contributors'] = self.contributors
		json_osf['title'] = self.title
		json_osf['description'] = self.description
		json_osf['id'] = self.id
		json_osf['url'] = 'http://clinicaltrials.gov/ct2/show/' + self.id
		json_osf['tags'] = self.keywords

		return json_osf

