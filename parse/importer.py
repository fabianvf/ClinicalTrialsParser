import json
import hmac
import hashlib
import requests
from glob import glob
from clinical_trials_parser import json_osf_format

API_URL='http://localhost:5000/api/v1/'
API_KEY='secret'

# Takes a python object as a payload
def get_project_signature(payload):
    signature = hmac.new(
        key=API_KEY,
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    return signature

def get_file_signature(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    signature = hmac.new(
        key=API_KEY,
        msg=data,
        digestmod=hashlib.sha256
    ).hexdigest()

    return signature

trials = glob('xml/*')
for trial in trials:
    id = trial.split('/')[-1].rstrip('.xml')
    project = json_osf_format(id)
    if not project:
        continue
    raw = json.dumps(project)
        
    signature = get_project_signature(raw)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'OSF {0}'.format(signature)}
    r = requests.post(API_URL+'project/import/', data=raw, headers=headers)
    
    response = json.loads(r.text)    
    projectTitle = project['title']

    files = project.get('files')
    if files:
        for f in files:
            files = {'file': (f.split('/')[-1], open(f, 'rb'))}
            signature = get_file_signature(f)
            headers = {'Authorization': 'OSF {0}'.format(signature)}
            r = requests.put(API_URL+'project/{pid}/node/{nid}/upload/'.format(
                pid=response[projectTitle]['id'],
                nid=response[projectTitle]['components']['Archive']['id']
            ),
            headers=headers, files=files)
