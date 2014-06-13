import requests
import json
from lxml import etree

#TODO: Write test code.



class ClinicalTrialData(object):
    """Parses an XML file containing clinical trial study data from clinicaltrials.gov"""
    def __init__(self,file_name):
        """Upon init, reads XML file,and parses it for some key information.
        NOTE: Comment tags are included in the XML tree."""
        self.file_name = str(file_name)
        self.root = etree.parse(self.file_name).getroot()
        self.id = self.root.find('id_info').find('nct_id').text
        self.url = self.root.find('required_header').find('url').text
        self.current_status = self.root.find('overall_status').text
        self.phase = self.root.find('phase').text
        self.description = self.root.find('brief_summary')[0].text

        if self.root.find('official_title') == None:
            self.title = self.root.find('brief_title').text
        else:
            self.title = self.root.find('official_title').text

        self.contributors = []
        for entry in self.root.findall('overall_official'):
            try:
                official_dict = {}
                official_dict['full_name'] = entry.find('last_name').text
                official_dict['role'] = entry.find('role').text
                official_dict['affiliation'] = entry.find('affiliation').text
                official_dict['email'] = None
            except AttributeError:
                pass
            self.contributors.append(official_dict)
        
        self.keywords = ["clinical trial"]
        for entry in self.root.findall('keyword'):
            self.keywords.append(entry.text)
        
        self.date_processed = self.__process_date()

        self.references = []
        for entry in self.root.findall('reference'):
            reference_dict = {'PMID':None}
            reference_dict['citation'] = entry.find('citation').text
            if entry.find('PMID') != None:
                reference_dict['PMID'] = entry.find('PMID').text
            self.references.append(reference_dict)
            
        self.locations = []     
        for entry in self.root.findall('location'):
            location_dict = {'name': None, 'zip': None, 'city': None, 'state': None, 'country': None}
            if entry.find('facility').find('name') != None:
                location_dict['name'] = entry.find('facility').find('name').text
            if entry.find('facility').find('address').find('zip') != None:
                location_dict['zip'] = entry.find('facility').find('address').find('zip').text
            if entry.find('facility').find('address').find('city') != None:
                location_dict['city'] = entry.find('facility').find('address').find('city').text
            if entry.find('facility').find('address').find('country') != None:
                location_dict['country'] = entry.find('facility').find('address').find('country').text
            if entry.find('facility').find('address').find('state') != None:
                location_dict['state'] = entry.find('facility').find('address').find('state').text
            self.locations.append(location_dict)


    def __process_date(self):
        """Private method for parsing the xml for the date processed (by clinicaltrials.gov) info."""
        date_string = self.root.find('required_header').find('download_date').text
        date_string = date_string.replace('ClinicalTrials.gov processed this data on ', '')
        return date_string

    def json_osf_format(self):
        """Returns a dictionary that represents key information about the clinical trial in json format."""
        json_osf = {
            "imported_from": "clinicaltrials.gov",
            "date_processed": self.date_processed,
            "contributors": self.contributors,
            "description": self.description,
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "files": [('../ct_xml/' + str(self.id) + '.xml'), ('../ct_raw_json/' + str(self.id) + '_raw.json' )],
            "tags": [
                "clinical trial"
            ],
            "phase": self.phase,
            "current_status": self.current_status,
            "geo_data": self.locations,
            "references": self.references,
            "components": [{"title":"MetaData","description":None}]
        }
        json_osf['tags'] = self.keywords
        return json_osf

    def json_osf_to_txt(self):
        """Writes the json returned by json_osf_format() to a text file."""
        with open((str(self.id) + '_osf.json'), 'w') as json_txt:
            json.dump(self.json_osf_format(), json_txt, sort_keys=True, indent=4)


