## parsing HTML files to pull out the xml data


''' XML location within HTML: 
body -> 2nd div id="sdiff-links" -> form -> 4th div id="sdiff-full" -> 
table -> tbody -> 
tr class = "sdiff-unc" or class = "sdiff-add" or class = "sdiff-chg" 
''' 

from bs4 import BeautifulSoup
import re

# testing on the first change file for NCT00000122
soup = BeautifulSoup(open("./ct_changes/NCT00000122/2005_06_30.html")) 

# this is a bs4 Tag object of just the sdiff-full stuff
sdiff_full = soup.find(id="sdiff-full")

# and these are the <tr> tags in that object with the xml we want
sdiff_xml = sdiff_full.find_all("tr", {"class" : 
                                ["sdiff-unc", "sdiff-add","sdiff-chg"]})

### td class sdiff-a: all of the "before" xml ###
all_before = []

for result in sdiff_xml:
    all_before.append(result.find("td", {"class" : "sdiff-a"}))


before_file = open('before.xml', 'w')

for item in all_before:
    before_file.write("%s\n" % item.text)


# td class sdiff-b: all of the "after" xml
all_after = []

for result in sdiff_xml:
    all_after.append(result.find("td", {"class" : "sdiff-b"}))

after_file = open('after.xml', 'w')

for item in all_after:
    after_file.write("%s\n" % item.text)
