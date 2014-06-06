
static_map = "http://maps.googleapis.com/maps/api/staticmap?size=600x600&markers="

list_of_tuples =[("Saint Vincent's Hosp and Med Ctr", "10011"), ("Univ of Cincinnati", "452670560"), ("Vanderbilt School of Medicine", "37232")]

marker_list = []

for element in list_of_tuples:
	marker = "|" + element[0].replace(" ", "+") +"+"+ element[1]
	marker_list.append(marker)

for element in marker_list:
	static_map+=element

print static_map
