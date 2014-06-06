import requests
import json
import time
from clinical_trials_ext import ClinicalTrialData

class bulk_trials(object):
	def __init__(self, id_list, first_time_bool):
		self.id_list=id_list
		self.url = None
		self.req = None
		self.json = None
		self.time_and_ctd = []
		self.timestamp = time.time()

		if(first_time_bool==True):
			with open("ClinicalTrialsTime.txt", 'w') as time_file:
				time_file.write(repr(self.timestamp))
		else:
			with open("ClinicalTrialsTime.txt", 'r') as time_file:
				self.old_time=time_file.read()
			with open("ClinicalTrialsTime.txt", 'w') as time_file:
				time_file.write(repr(self.timestamp))
	
	def create_CT_list(self):
		"""Returns a list of ClinicalTrialData objects created from the json returned by the Lilly API 
			(which contains the id's of several different trials)."""
		i=0
		ct_list=[]

		while i < len(self.id_list):
			self.url="http://api.lillycoi.com/v1/trials/"+ self.id_list[i][0] + ".json"
			self.req=requests.get(self.url)
			self.json=self.req.json()
			ct =  ClinicalTrialData(self.id_list[i][0])
			time = self.id_list[i][1]
			self.time_and_ctd.append([self.id_list[i][0], time])
			ct_list.append(ct)
			i+=1

		return ct_list

	def create_timestamp_list(self):
		i=0
		ct_time_list=[]

		while i < len(self.id_list):
			self.url="http://api.lillycoi.com/v1/trials/"+ self.id_list[i][0] + ".json"
			self.req=requests.get(self.url)
			self.json=self.req.json()
			ct =  self.id_list[i]
			ct_list.append(ct)
			i+=1

		return ct_list




			
a = [["NCT00552448", "time1"], ["NCT00000116", "time2"]]
q = bulk_trials(a, True)
#print q.old_time
ll = q.create_CT_list()
# print len(ll)
# print ll[0].description
# print q.time_and_ctd
# print ll[1].description

