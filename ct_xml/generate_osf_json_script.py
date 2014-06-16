from clinical_trials_parser import ClinicalTrialData


""" Takes a text file named "key_studies.txt" as input, extracts the nct_id's listed in the file, and generates json files in OSF format from the XML file with the corresponding nct_id number."""

id_list = []

with open('key_studies.txt', 'r') as key_studies:
	key_studies = key_studies.readlines()
	for nct_id in key_studies:
		id_list.append(nct_id.rstrip('\n'))

for nct_id in id_list:
	ClinicalTrialData(nct_id+'.xml').json_osf_to_txt()
