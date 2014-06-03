import requests
import json
import time
import datetime

class ClinicalTrialData(object):
	"""Uses the Lilly COI API to GET clinical trial study data in the form of Json."""
	def __init__(self,id):
		self.id = id
		self.url = 'http://api.lillycoi.com/v1/trials/' + id + '.json'
		self.request = requests.get(self.url)
		self.json = self.request.json()
		self.title = self.json['results'][0]['official_title']
		self.description = self.json['results'][0]['brief_summary']['textblock']

		try:
			if self.has_first_name():
				self.author_name = self.json['results'][0]['overall_official'][0]['first_name'] + self.json['results'][0]['overall_official'][0]['last_name']
			else:
				self.author_name = self.json['results'][0]['overall_official'][0]['last_name']
		except IndexError:
			self.author_name = "Not provided"
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		self.pullDate=st;

	def json_to_txt(self):
		with open((self.id + '.json'), 'w') as json_txt:
			json.dump(self.json, json_txt, sort_keys=True, indent=4)
	def has_first_name(self):
		if self.json['results'][0]['overall_official'][0]['first_name'] == None:
			return False
		else:
			return True

	#def create_json_template(self):
	#	with open("text.json", "w") as outfile:
	#		json.dump({'source': self.json['results'][0]['source'], 'contributors':self.author_name, 'description':self.description, 'tags':self.json['results'][0]['keyword']}, outfile, indent=2)


#ctd = ClinicalTrialData('NCT00042289')
#ctd.create_json_template()