import requests
import json

class ClinicalTrialData(object):
	"""Uses the Lilly COI API to GET clinical trial study data in the form of Json."""
	def __init__(self,id):
		self.id = id
		self.url = 'http://api.lillycoi.com/v1/trials/' + id + '.json'
		self.request = requests.get(self.url)
		self.json = self.request.json()
		self.title = self.json['results'][0]['official_title']
		self.description = self.json['results'][0]['brief_summary']['textblock']
		if self.has_first_name():
			self.author_name = self.json['results'][0]['overall_official'][0]['first_name'] + self.json['results'][0]['overall_official'][0]['last_name']
		else:
			self.author_name = self.json['results'][0]['overall_official'][0]['last_name']
	def json_to_txt(self):
		with open((self.id + '.json'), 'w') as json_txt:
			json.dump(self.json, json_txt, sort_keys=True, indent=4)
	def has_first_name(self):
		if self.json['results'][0]['overall_official'][0]['first_name'] == None:
			return False
		else:
			return True