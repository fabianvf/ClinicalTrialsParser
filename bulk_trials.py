import requests
import json
from clinical_trials_ext import ClinicalTrialData
class bulk_trials(object):
	def __init__(self, offset, limit):
		self.offset=offset
		self.limit=limit
		self.url="http://api.lillycoi.com/v1/trials.json?offset=" + str(offset) + "&limit=" + str(limit)
		self.req=requests.get(self.url)
		self.json=self.req.json()
		self.id = None
	

	def create_CT_list(self):

		i=0

		ct_list=[]

		while i < self.limit:
			ct =  ClinicalTrialData(self.json['results'][i]['id'])
			ct_list.append(ct)
			i+=1

		return ct_list

			

q = bulk_trials(4, 100)
ll = q.create_CT_list()
print len(ll)

