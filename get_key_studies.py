# python script to take a list of IDs from a file list
# and save those as XML documnetns from ClinicalTrials.org

import requests
import zipfile
import time
import xml.etree.ElementTree as ET, glob
import os

def save_key_zipfiles():

    key_id_file = 'key_studies.txt'
    key_id_folder = 'key_xml_files/'

    with open (key_id_file) as key_ids:
            key_id_list = [line.strip() for line in key_ids]

    base_url = 'http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=results&down_flds=shown&down_fmt=plain&id='

    end = '&show_down=Y'

    for item in key_id_list:
        url_id = item
        url = base_url + url_id + end
        key_xml = requests.get(url)

        # save that xml to a zip file
        with open(key_id_folder + item + ".zip", "wb") as results:
            results.write(key_xml.content)

        # wait 3 seconds between requests to be nice :)
        time.sleep(3)

def unzip_key_files():

    key_zip_folder = 'key_xml_files/'
    ziplist = glob.glob(key_zip_folder + '*.zip')

    # loop over all of the zip files in the updated catalog
    for filename in ziplist:
        with zipfile.ZipFile(filename) as zf:
            zf.extractall(key_zip_folder)

    # now delete all the zip files! 
    for zip_file in ziplist:
        os.remove(zip_file)

save_key_zipfiles()
unzip_key_files()
