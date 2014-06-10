import json
from bs4 import BeautifulSoup




"""returns a list of pubmed ids from a single clinical trial"""
def other_publications(jsonFile):
	pmid_list=[]
	json_file = open(jsonFile).read()
	json_data = json.loads(json_file)
	for d in json_data['references']:
		pmid_list.append(d['PMID'])
	return pmid_list

def bulk_other_publications(json_list):
	dict_of_pmids={}
	for j in json_list:
		pmid = other_publications(j)
		dict_of_pmids[j]=pmid
	print dict_of_pmids

#bulk_other_publications(["NCT00000162_osf.json", "NCT00000122_osf.json"])

