''' both returns and saves a list of all IDs in the clinical trials API '''

import requests
import json

def get_all_ids():

	# get the total number of ids in the API
	url = 'http://api.lillycoi.com/v1/trials.json?fields=id'
	initial = requests.get(url)
	initial_json = initial.json()
	total = initial_json['totalCount']

	# the real request using the total from the first request
	all_url = 'http://api.lillycoi.com/v1/trials.json?limit=' + str(total) + '&fields=id'
	all_ids = requests.get(all_url)
	id_json = all_ids.json()

	ids = id_json['results']

	# make a list of just all the IDs
	id_list = []
	for item in ids:
		id_list.append(item.get('id'))

	# save that ID list to a file
	file_name = open('all_ids.txt', 'w')
	for item in id_list:
		file_name.write("%s\n" % item)

	return id_list


get_all_ids()
