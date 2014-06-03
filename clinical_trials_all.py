import requests
import json

offset = '0'
count = 10
file_name = 'all.json'

url = 'http://api.lillycoi.com/v1/trials.json?offset=' + offset

initial_request = requests.get(url)

request_json = initial_request.json()

total = request_json['totalCount']


next_url = request_json['nextPageURI']


# just for testing so we don't get all zillion trials
soft_total = 50

IDs = []


## for each trial in the set
while count <= soft_total:
	next_url = request_json['nextPageURI']

	with open(file_name, 'w') as json_txt:
			json.dump(request_json, json_txt, sort_keys=True, indent=4)

	url = next_url
	next_request = requests.get(url)
	request_json = next_request.json()

	count += 10
