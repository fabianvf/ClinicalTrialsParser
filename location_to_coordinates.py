import requests
import json


def GetCoordinates(city, country, zip=None, state=None):
    """Takes location data (city, state, zip, country) as input. Sends a GET request to the open street maps/mapquest API and 
    pulls latitude/longitude information out of the Json that's returned."""

    url = 'http://open.mapquestapi.com/nominatim/v1/search.php'
    parameters = {'city': city, 'country': country, 'postalcode': None, 'state': state, 'format': 'json' }
#   if country == 'United States':
#       parameters['postalcode'] = zip
    request = requests.get(url, params=parameters)
    request_json = request.json()
    return {'latitude': request_json[0]['lat'], 'longitude': request_json[0]['lon']}


def LocationToCoord(file_name):
    """Takes an {nct_id}_osf.json file name as input. Extracts the geo_data, adds longitude and latitude data to it, and returns
    the geo_data with longitude and latitude added in."""
    json_osf = open(file_name, 'r')
    json_osf = json.load(json_osf)
    json_osf_locations = json_osf['geo_data']
    for location in json_osf_locations:
        coordinates = GetCoordinates(location['city'], location['country'], zip=str(location['zip']), state=location['state'])
        location['latitude'] = coordinates['latitude']
        location['longitude'] = coordinates['longitude']
    return json_osf_locations

print LocationToCoord('NCT02147249_osf.json')
print LocationToCoord('NCT00000201_osf.json')
print LocationToCoord('NCT00000193_osf.json')