''' Script to check for new studies that have been updated the day before '''

import requests
import datetime
import zipfile

''' download and save a zipfile of new results '''
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

''' save and return a list of all new file names '''
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

get_new_results()

newfile_names()
