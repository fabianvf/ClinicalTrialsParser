''' Script to check for updates to just our 10 key studies '''

import requests
import datetime
import zipfile

# download and save a zipfile of new results
def get_new_results():

    # date for today 
    today = datetime.date.today()

    month = today.strftime('%m')
    day = today.strftime('%d')
    year = today.strftime('%Y')

    # date for yesterday
    yesterday  = today - datetime.timedelta(1)

    y_month = yesterday.strftime('%m')
    y_day = yesterday.strftime('%d')
    y_year = yesterday.strftime('%Y')

    # use those in the URL to create for requests
    base_url = 'http://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=results&down_flds=shown&down_fmt=plain&lup_s=' 

    sep = '%2F'
    middle = '&lup_e='
    end = '&show_down=Y'

    url_end = y_month + sep + y_day + sep + y_year + middle + month + sep + day + sep + year + end

    url = base_url + url_end

    # get the new results
    new_results = requests.get(url)

    # save those new results to a zip file
    with open("new_results.zip", "wb") as results:
        results.write(new_results.content)

# save and return a list of all new file names
def newfile_names():

    new_id_list = []

    try: 
        zipped_results = zipfile.ZipFile('new_results.zip')
        new_id_list = zipped_results.namelist()

    except BadZipfile, e:
        print "zipfile is empty. Excepton: " + e

    # also save that ID list to a file
    file_name = open('new_ids.txt', 'w')
    for item in new_id_list:
        file_name.write("%s\n" % item)

    return new_id_list

# returns a list of updated key files
def check_key_files():

    key_id_file = 'key_studies.txt'

    get_new_results()

    new_id_list = newfile_names()
    # gets rid of the xml selections
    new_id_list = [ext.replace('.xml','') for ext in new_id_list]

    with open (key_id_file) as key_ids:
        key_id_list = [line.strip() for line in key_ids]

    key_updated_files = list(set(new_id_list).intersection(key_id_list))

    # also save key updated IDs to a file
    file_name = open('updated_key_ids.txt', 'w')
    for item in key_updated_files:
        file_name.write("%s\n" % item)

    return key_updated_files

check_key_files()

