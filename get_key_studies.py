# python script to take a list of IDs from a file list
# and save those as XML documnetns from ClinicalTrials.org

import requests
import zipfile
import time
import glob
import os

''' usage: id_file is the file containing IDs, the  '''
def save_key_zipfiles(id_file):

    key_id_folder = 'ct_xml/'

    with open (id_file) as key_ids:
            key_id_list = [line.strip().replace('\xe2\x80\xa8', '' ) for line in key_ids]
            print key_id_list

    base_url = 'http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=results&down_flds=shown&down_fmt=plain&id='

    end = '&show_down=Y'

    for url_id in key_id_list:
        url = base_url + url_id + end
        key_xml = requests.get(url)

        # save that xml to a zip file
        with open(key_id_folder + url_id + ".zip", "wb") as results:
            results.write(key_xml.content)

        # wait 3 seconds between requests to be nice :)
        time.sleep(3)

def unzip_key_files():

    key_zip_folder = 'ct_xml/'
    ziplist = glob.glob(key_zip_folder + '*.zip')

    # loop over all of the zip files in the updated catalog
    for filename in ziplist:
        try:
            with zipfile.ZipFile(filename) as zf:
                zf.extractall(key_zip_folder)
        except BadZipfile:
            pass

    # now delete all the zip files! 
    for zip_file in ziplist:
        os.remove(zip_file)
# 
save_key_zipfiles('key_studies.txt')
unzip_key_files()
