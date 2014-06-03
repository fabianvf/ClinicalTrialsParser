from clinical_trials_ext import ClinicalTrialData
import unittest
import requests

id = 'NCT01578525'
ctd_obj = ClinicalTrialData(id)


class TestClinicalTrialData(unittest.TestCase):
	""" Takes a ClinicalTrialsData object as input and runs several test cases on it."""
	def runTest(self):
		self.test_ctd_has_json()
		self.test_ctd_has_title()
		self.test_ctd_has_description()
		self.test_has_name()
		print 'Tests All Passed!'
	def test_ctd_has_json(self):
		self.assertEqual(ctd_obj.json, requests.get(ctd_obj.url).json())
	def test_ctd_has_title(self):
		self.assertEqual(ctd_obj.title, ctd_obj.json['results'][0]['official_title'])
	def test_ctd_has_description(self):
		self.assertEqual(ctd_obj.description, ctd_obj.json['results'][0]['brief_summary']['textblock'])
	def test_has_name(self):
		if ctd_obj.has_first_name():
			full_name = ctd_obj.json['results'][0]['overall_official'][0]['first_name'] + ctd_obj.json['results'][0]['overall_official'][0]['last_name']
			self.assertEqual(ctd_obj.author_name, full_name)
		else:
			self.assertEqual(ctd_obj.author_name, ctd_obj.json['results'][0]['overall_official'][0]['last_name'])
			
tester = TestClinicalTrialData()
tester.runTest()