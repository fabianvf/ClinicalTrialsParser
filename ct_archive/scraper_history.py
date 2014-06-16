__author__ = 'faye'

from parser_date import *
import requests
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getIDs():
    allIds = []
    fileIds = open('partial_ids.txt', 'r')

    for line in fileIds:
        lineId = line.split()
        lineClean = lineId[0].translate(None, "[',u")
        allIds.append(lineClean)

    return allIds

allIds = getIDs()

for id in allIds:
    myReq = requests.get('http://clinicaltrials.gov/archive/'+id)

    if not os.path.exists("ct_dates/"+id):
        os.makedirs("ct_dates/"+id)

    f = open("ct_dates/"+id+"/"+id+".html", 'w')
    f.write(myReq.text)
    f.close()
    print id+" dates collected."

    soup = BeautifulSoup(open('ct_dates/'+id+'/'+id+'.html'))

    dates = getDates(soup)

    for date in dates:
        reqStudy = requests.get('http://clinicaltrials.gov/archive/'+id+'/'+date)

        if not os.path.exists("ct_studies/"+id):
            os.makedirs("ct_studies/"+id)

        f = open("ct_studies/"+id+"/"+date+".html", 'w')
        f.write(reqStudy.text)
        f.close()
        print id+" studies collected."

    dates.pop(0)

    for date in dates:
        reqChanges = requests.get('http://clinicaltrials.gov/archive/'+id+'/'+date+'/changes')

        if not os.path.exists("ct_changes/"+id):
            os.makedirs("ct_changes/"+id)

        f = open("ct_changes/"+id+"/"+date+".html", 'w')
        f.write(reqChanges.text)
        f.close()
        print id+" changes collected."
