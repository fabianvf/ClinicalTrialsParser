from bs4 import BeautifulSoup
from ct_timeline_parser import *
from ct_archive.parser_date import *
from ct_timeline import text_generator
import os
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def generateJSON(soup, articleSoupList, articleId):
    compiledJSON = []
    articleList = []

    compiledJSON.append(getTitle(soup))
    compiledJSON.append('"type":"default"')
    compiledJSON.append(getText(soup))
    compiledJSON.append(getStartDate(soup))
    for articleSoup in articleSoupList:
        articleDate = articleSoup.find("th", text="Updated:").next_sibling.string
        ct_article = '{'+getArticleEvent(getArticleStartDate(articleSoup),getArticleHeadline(articleSoup),getArticleText(articleId,articleDate),getAsset())+'}'
        articleList.append(ct_article)
    compiledJSON.append('"date": ['+','.join(articleList)+']')
    return ",".join(compiledJSON)

def generateHTML(articleId):
    soup = BeautifulSoup(open("../TimelineJS/examples/example_json.html"))
    scriptTag = soup.script
    scriptTag.string = '\n        var timeline_config = {\n         width: "100%",\n         height: "100%",\n         source: "'+articleId+'.json"\n        }\n      '
    return soup

articleList = []
key_list = []
key_studies = open("../key_studies.txt",'r')
for key in key_studies:
    key_list.append(key.rstrip())

text_generator.ct_text_generator(key_list)

for key in key_list:
    soup = BeautifulSoup(open('../ct_archive/ct_dates/'+key+'/'+key+'.html'))
    articleSoupDates = getDates(soup)
    for date in articleSoupDates:
        articleSoup = BeautifulSoup(open('../ct_archive/ct_studies/'+key+'/'+date+'.html'))
        articleList.append(articleSoup)

    finalJSON = '{"timeline":{'+generateJSON(soup, articleList, key)+'}}'

    if not os.path.exists("../ct_timeline/ct_articles/"+key+"/"):
        os.makedirs("../ct_timeline/ct_articles/"+key+"/")
    f = open("../ct_timeline/ct_articles/"+key+"/"+key+".json", 'w')
    f.write(finalJSON)
    f.close()

    f = open("../ct_timeline/ct_articles/"+key+"/"+key+".html", 'w')
    f.write(str(generateHTML(key)))

    del articleList[:]

    print "HTML & JSON Generated"