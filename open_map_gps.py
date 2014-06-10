import requests
import json
from lxml import etree


"""gets the gps coordinates of a given place and zipcode, for example:"""
"""get_coordinate(woodson high school 22032)"""
def get_coordinate(address):

	url = "http://nominatim.openstreetmap.org/search?q="
	a = address.replace(" ", "+")
	r = requests.get(url+a+"&format=xml").text
	root = etree.fromstring(r.encode("utf-8"))
	place = root.find('place').attrib
	lat = place['lat']
	lon = place['lon']
	return lat+ " " +lon

