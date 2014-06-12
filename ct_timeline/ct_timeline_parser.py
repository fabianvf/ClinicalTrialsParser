from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getTitle(soup):
    title = soup.find(class_="metadata").b.next_sibling
    return '"headline":"'+title+'"'

def getText(soup):
    text = soup.find("h1").string
    return '"text":"'+text+'"'

def getStartDate(soup):
    #    startDate = soup.find_all(class_="si-date")
    dates = []
    for date in soup.find_all(class_="si-date"):
        dates.append(str(date.string))
    startDate = dates[1].replace("_",",")
    return '"startDate":"'+startDate+'"'

def getArticleStartDate(soup):
    date = soup.find("th", text="Updated:").next_sibling.string
    startDate = date.replace("_",",")
    return '"startDate":"'+startDate+'"'

def getArticleHeadline(soup):
    headline = soup.find('h1').string
    headline = " ".join(headline.split())
    return '"headline":"'+headline+'"'

def getArticleText(id, date):
    text = open("ct_text/"+id+"/"+date+".html")
    fullText = text.read()
    fullText = json.dumps(fullText)
    return '"text":'+fullText

#TODO I need Erin's XML Input
def getAsset():
    return '"asset":{"media":"","credit":"clinicaltrials.gov","caption":""}'

def getArticleEvent(startDate, headline, text, asset):
    fullArticle = []
    fullArticle.append(startDate)
    fullArticle.append(headline)
    fullArticle.append(text)
    fullArticle.append(asset)
    return ",".join(fullArticle)

soup = BeautifulSoup(open('../ct_archive/ct_dates/NCT00000122/NCT00000122.html'))
articleSoup = BeautifulSoup(open('../ct_archive/ct_studies/NCT00000122/2005_06_23.html'))

#print getTitle(soup)
#print getText(soup)
#print getStartDate(soup)
#print getArticleStartDate(articleSoup)
#print getArticleHeadline(articleSoup)
#print getArticleText(articleSoup)
#print getArticleEvent(getArticleStartDate(articleSoup),getArticleHeadline(articleSoup),getArticleText(articleSoup),getAsset())