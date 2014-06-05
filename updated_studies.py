''' Script to check for new studies that have been updated the day before '''

import requests
import datetime

def get_new_results():

    ''' first, figure out the date of today and yesterday 
    to use in the request URL '''

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

    ''' Then, use that URL to download a ZIP file of new results '''

    # get the new results
    new_results = requests.get(url)

    with open("new_results.zip", "wb") as results:
        results.write(new_results.content)

get_new_results()