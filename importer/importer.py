import json
import hmac
import hashlib
import requests
from collections import OrderedDict


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

f = open('../ct_archive/CTgov_study_NCT00001372.json', 'r')
raw = f.read()
signature = get_project_signature(raw)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'OSF {0}'.format(signature)}
r = requests.post(API_URL+'project/import/', data=raw, headers=headers)
print r.text
response = json.loads(r.text)

projectTitle = json.loads(raw)['title']

#print response[projectTitle]['components']['Introduction']['id']

fileName = []
project = json.loads(raw)
#for project in projects:
if project.get('files'):
    fileName.append(project['files'])
    for f in fileName: # TODO better file uploading
        files = {'file': (f, open(f, 'rb'))}
        signature = get_file_signature(f)
        headers = {'Authorization': 'OSF {0}'.format(signature)}
        r = requests.put(API_URL+'project/{pid}/node/{nid}/upload/'.format(
                pid=response[projectTitle]['id'],
                nid=response[projectTitle]['components']['MetaData']['id']
            ),
            headers=headers, files=files)
    for component in project['components']:
        if component.get('files'):
            files = files + component['files']



            # now upload a file to a node (project or component)
print r.text
