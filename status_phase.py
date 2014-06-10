import json

"""Gets the status of a single trial"""
def get_status(jsonFile):
	json_file = open(jsonFile).read()
	json_data = json.loads(json_file)
	return json_data['current_status']


"""Gets the phase of a single trial"""
def get_phase(jsonFile):
	json_file = open(jsonFile).read()
	json_data = json.loads(json_file)
	return json_data['phase']


"""Prints out count of how many trials in each status"""
def bulk_get_status(json_list):
	status_list={"Not yet recruiting": 0, "Recruiting":0,"Available for expanded access":0, 
	"Active, not recruiting":0, "Completed":0,
	"Terminated":0,"Suspended":0,"Withdrawn":0,"Enrolling by invitation":0, 
	"Temporarily not available for expanded access":0,
	"Temporarily not available for expanded access":0,"No longer available for expanded access":0,
	"Approved for marketing":0,"Unknown":0, "N/A":0}
	for trial in json_list:
		j_file=get_status(trial)
		if(j_file in status_list):
			status_list[j_file]+=1;
		else:
			status_list[j_file]=1;
	print status_list

"""Gets the phase for a list of trials"""

def bulk_get_phase(json_list):
	phase_list=[]
	for j in json_list:
		json_file = get_phase(j)
		phase_list.append(json_file)
	print phase_list
