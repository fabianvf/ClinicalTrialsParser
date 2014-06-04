''' both returns and saves a list of all IDs in the clinical trials API '''

import requests
import json
import time

def get_all_ids():

	limit = 10000
	offset = 0

	# get the total number of ids in the API
	url = 'http://api.lillycoi.com/v1/trials.json?fields=totalCount'
	initial = requests.get(url)
	initial_json = initial.json()
	total = initial_json['totalCount']
	time.sleep(1)

	id_list = []

	while offset < total:
		partial_url = 'http://api.lillycoi.com/v1/trials.json?limit=' + str(limit) + '&fields=id&offset=' + str(offset)
		partial_ids = requests.get(partial_url)
		partial_ids_json = partial_ids.json()
		partial_ids = partial_ids_json['results']

		for item in partial_ids:
			id_list.append(item.get('id'))

		print "got " + str(offset) + " trials!"

		offset += limit

		time.sleep(3)

	# save that ID list to a file
	file_name = open('all_ids.txt', 'w')
	for item in id_list:
		file_name.write("%s\n" % item)

	return id_list

get_all_ids()
