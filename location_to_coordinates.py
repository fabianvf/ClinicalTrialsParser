import requests
import json

def GetCoordinates(city, country, zip=None, state=None):
	"""Takes location data (city, state, zip, country) as input. Sends a GET request to the open street maps/mapquest API and 
	pulls latitude/longitude information out of the Json that's returned."""

	url = 'http://open.mapquestapi.com/nominatim/v1/search.php'
	parameters = {'city': city, 'country': country, 'postalcode': None, 'state': state, 'format': 'json' }
	if country == 'United States':
		parameters['postalcode'] = zip
	request = requests.get(url, params=parameters)
	request_json = request.json()
	return {'latitude': request_json[0]['lat'], 'longitude': request_json[0]['lon']}


json_cord = GetCoordinates('Baltimore', 'United States', state="MD", zip='21224 6823')

print json_cord
                          