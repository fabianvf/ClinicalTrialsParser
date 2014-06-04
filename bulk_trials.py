import requests
import json
from clinical_trials_ext import ClinicalTrialData
class bulk_trials(object):
	def __init__(self, id_list):
		self.id_list=id_list
		self.url = None
		self.req = None
		self.json = None

	def create_CT_list(self):

		i=0

		ct_list=[]

		while i < len(self.id_list):
			self.url="http://api.lillycoi.com/v1/trials/"+ self.id_list[i] + ".json"
			self.req=requests.get(self.url)
			self.json=self.req.json()
			ct =  ClinicalTrialData(self.id_list[i])
			ct_list.append(ct)
			i+=1

		return ct_list

			
#a = ["NCT00552448", "NCT00000116"]
#q = bulk_trials(a)
#ll = q.create_CT_list()
#print len(ll)
#print ll[0].description
#print ll[1].description

