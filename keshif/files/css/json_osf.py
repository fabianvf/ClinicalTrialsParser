## to save all the json on the osf to a file...

import requests
import json

osf_json = requests.get('https://api.myjson.com/bins/4l9gb')

# all_json is a list, one element per trial
# each element is a bunch of json
all_json = osf_json.json()

# returns only the most recent trial key

recent_trial_keys = []
for item in all_json:
    recent_trial_keys.append(sorted(item.keys())[-1])

recent_trials = []
for index, item in enumerate(all_json):
    recent_trials.append(item[recent_trial_keys[index]])



