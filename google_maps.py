"""Takes a list of tuples, with each tuple consisting of a location and its zip code, as input and generates the url for a static google map using it."""

def GetStaticMap(location_tuples = [("Saint Vincent's Hosp and Med Ctr", "10011")]):
	static_map_url = "http://maps.googleapis.com/maps/api/staticmap?size=600x600&markers="
	marker_list = []
	for element in location_tuples:
		marker = "|" + element[0].replace(" ", "+") +"+"+ element[1]
		static_map_url += marker
	return static_map_url

print GetStaticMap()

API_KEY = "AIzaSyCpm3h6R-8AikVqTxPVKO9x9bmYL8vNA14"

def GetDynamicMap( API_KEY, location_tuple=("Saint Vincent's Hosp and Med Ctr", "10011")):
	dynamic_map_url =  "https://www.google.com/maps/embed/v1/place?key=" + API_KEY + "" 
	marker = "&q=" + location_tuple[0].replace(" ", "+") + "+" + location_tuple[1]
	dynamic_map_url += marker
	return dynamic_map_url

print GetDynamicMap(API_KEY)