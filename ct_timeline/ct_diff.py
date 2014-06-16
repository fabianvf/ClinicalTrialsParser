from bs4 import BeautifulSoup
from ct_archive import parser_date
from difflib import *
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import diff_match_patch

def ct_diff(soupA, soupB):
    bodyA = soupA.find(class_="info")
    bodyB = soupB.find(class_="info")

    diff = HtmlDiff()

    #finalHtml = diff.make_file(str(bodyA).splitlines(), str(bodyB).splitlines())

    dmp = diff_match_patch.diff_match_patch()
    diffs = dmp.diff_main(str(bodyA), str(bodyB))
    dmp.diff_cleanupSemantic(diffs)
    htmlSnippet = dmp.diff_prettyHtml(diffs)
    htmlSnippet = htmlSnippet.replace("&para;", "")
    htmlSnippet = htmlSnippet.replace("<br>", "")
    #htmlSnippet = unicode(htmlSnippet, "UTF-8")
    #htmlSoup = BeautifulSoup(htmlSnippet)
    #finalHtml = htmlSoup.prettify(formatter="html")
    finalHtml = BeautifulSoup(htmlSnippet)
    finalHtmlUpdate = finalHtml.find_all("del")

    for deletedText in finalHtmlUpdate:
        if "&lt;td&gt;" in str(deletedText.get_text):
            updatedDeletedText = str(deletedText).replace("&gt;",'&gt;<del style="background:#ffe6e6">')
            updatedDeletedText = str(updatedDeletedText).replace("&lt;", '</del>&lt;')
            finalHtml = str(finalHtml).replace(str(deletedText), str(updatedDeletedText))
    #finalHtml = finalHtml.find(class_="info")
    finalHtml = str(finalHtml).replace("&lt;", "<")
    finalHtml = str(finalHtml).replace("&gt;", ">")
    return finalHtml

def ct_diff_generator(key_list):
    for key in key_list:
        i = 0
        soup = BeautifulSoup(open("../ct_archive/ct_dates/"+key+"/"+key+".html"))
        dates = parser_date.getDates(soup)
        for date in dates:
            if date != dates[0]:
                soupA = BeautifulSoup(open("../ct_archive/ct_studies/"+key+"/"+dates[i]+".html", 'r'))
                soupB = BeautifulSoup(open("../ct_archive/ct_studies/"+key+"/"+date+".html", 'r'))
                souptest = ct_diff(soupA,soupB)
                if not os.path.exists("ct_diff/"+key+"/"):
                    os.makedirs("ct_diff/"+key+"/")
                f = open("ct_diff/"+key+"/"+date+".html", 'w')
                f.write(str(souptest))
                f.close()
                i += 1
                print str(key) +" "+ str(date) + " Diff Generated"