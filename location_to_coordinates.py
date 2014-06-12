import requests
import json

def GetCoordinates(city, country, location=None, zip=None, state=None):
	url = 'http://open.mapquestapi.com/nominatim/v1/search.php'
	parameters = {'city': city, 'country': country, 'postalcode': None, 'state': state, 'format': 'json' }
	if country == 'United States':
		parameters['postalcode'] = zip
	request = requests.get(url, params=parameters)
	request_json = request.json()
	return {'latitude': request_json[0]['lat'], 'longitude': request_json[0]['lon']}

json_cord = GetCoordinates('Baltimore', 'United States', state='Maryland', zip='21224 6823')

print json_cord
