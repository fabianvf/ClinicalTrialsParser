from bs4 import BeautifulSoup
from ct_archive import parser_date
from ct_timeline import ct_diff
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def ct_text_generator(key_list):

    htmlFinal = []

    ct_diff.ct_diff_generator(key_list)

    for key in key_list:
        soupDate = BeautifulSoup(open("../ct_archive/ct_dates/"+key+"/"+key+".html"))

        for date in parser_date.getDates(soupDate):
            if date == parser_date.getDates(soupDate)[0]:
                if not os.path.exists("ct_text/"+key+"/"):
                    os.makedirs("ct_text/"+key+"/")
                f = open("ct_text/"+key+"/"+date+".html", 'w')
                soupA = BeautifulSoup(open("../ct_archive/ct_studies/"+key+"/"+date+".html"))
                soupA = soupA.find(class_="info")
                f.write(str(soupA))
                f.close()
                print str(key) + " " + str(date) + " Text Generated"
            else:
                soupA = BeautifulSoup(open("../ct_archive/ct_studies/"+key+"/"+date+".html"))
                soupA = soupA.find(class_="info")
                htmlFinal.append('<body style="display:table; border-collapse:separate; border-spacing:10px;"><div class="separation" id="current" style="display: table-cell; padding: 10px; border: 3px; border-style: solid; border-color: #bbbbbb;">')
                htmlFinal.append(str(soupA))
                htmlFinal.append('</div><div class="separation" id="past" style="display: table-cell; padding: 10px; border: 3px; border-style: solid; border-color: #bbbbbb;">')
                soupB = BeautifulSoup(open("ct_diff/"+key+"/"+date+".html"))
                htmlFinal.append(str(soupB))
                htmlFinal.append('</div></body>')
                if not os.path.exists("ct_text/"+key+"/"):
                    os.makedirs("ct_text/"+key+"/")
                f = open("ct_text/"+key+"/"+date+".html", 'w')
                f.write(''.join(htmlFinal))
                f.close()
                del htmlFinal[:]
                print str(key) + " " + str(date) + " Text Generated"