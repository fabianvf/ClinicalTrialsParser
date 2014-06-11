import requests
import json
from lxml import etree


"""gets the gps coordinates of a given place and zipcode from LillyCOI api, for example:"""
"""get_coordinate(woodson high school 22032)"""
def get_coordinate(nct):
	nct_id=nct
	r = requests.get("http://api.lillycoi.com/v1/trials/" + nct + ".json")
	json = r.json()
	gps_dict={}
	for location in json['results'][0]['location']:
		lon = location['geodata']['longitude']
		lat = location['geodata']['latitude']
		name = location['facility']['name']
		gps_dict[name] = str(lat) + " " + str(lon)
	return gps_dict


#get_coordinate("NCT02155933")

