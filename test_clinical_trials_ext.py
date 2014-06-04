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
		self.test_has_contributors()
		self.test_json_osf_format()
		print 'Tests All Passed!'
	def test_ctd_has_json(self):
		self.assertEqual(ctd_obj.json, requests.get(ctd_obj.url).json())
	def test_ctd_has_title(self):
		self.assertEqual(ctd_obj.title, ctd_obj.json['results'][0]['official_title'])
	def test_ctd_has_description(self):
		self.assertEqual(ctd_obj.description, ctd_obj.json['results'][0]['brief_summary']['textblock'])
	def test_has_contributors(self):
		test_contributors = [
                {
                    "full_name": "Albrecht Eisert, Dr. rer. nat.", 
                    "role": "Study Director"
                }, 
                {
                    "full_name": "Axel Heidenreich, Prof. Dr. med.", 
                    "role": "Principal Investigator"
                }, 
                {
                    "full_name": "Joerg B Schulz, Prof. Dr. med.", 
                    "role": "Principal Investigator"
                }, 
                {
                    "full_name": "Christian Trautwein, Prof. Dr. med.", 
                    "role": "Principal Investigator"
                }, 
                {
                    "full_name": "Ulrich Jaehde, Prof. Dr. rer. nat.", 
                    "role": "Study Chair"
                }, 
                {
                    "full_name": "Rebekka Heumueller", 
                    "role": "Principal Investigator"
                }
                ]
		self.assertEqual(ctd_obj.contributors, test_contributors)
	def test_json_osf_format(self):
		test_osf_format = {
    		"source": "lilly",
            "time_retrieved": ctd_obj.time_stamp,
    		"contributors": ctd_obj.contributors,
    		"title": "Medication Safety of Elderly Patients in Hospital and Ambulatory Setting Considering the Transitions of Care for Home-cared Patients and Nursing Home Residents",
    		"description": "The purpose of this study is to determine whether additional pharmaceutical care for elderly\n      patients (home-cared patients, nursing-home residents) has a positive impact on drug-related\n      readmissions.",
    		"tags": [
                "clinical trial",
                "medication safety", 
                "elderly", 
                "pharmaceutical care", 
                "hospital readmission", 
                "drug-related readmission", 
                "Health Services for the Aged"
    		],
    		"id": 'NCT01578525',
    		"url": 'http://clinicaltrials.gov/ct2/show/NCT01578525'

		}
		self.assertEqual(ctd_obj.json_osf_format(), test_osf_format)

tester = TestClinicalTrialData()
tester.runTest()


