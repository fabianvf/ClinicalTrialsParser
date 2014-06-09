## parsing HTML files to pull out the xml data


''' XML location within HTML: 
body -> 2nd div id="sdiff-links" -> form -> 4th div id="sdiff-full" -> 
table -> tbody -> 
tr class = "sdiff-unc" or class = "sdiff-add" or class = "sdiff-chg" 
''' 

from bs4 import BeautifulSoup

# testing on the first change file for NCT00000122
soup = BeautifulSoup(open("./ct_archive/ct_changes/NCT00000122/2005_06_30.html")) 

# this is a bs4 Tag object of just the sdiff-full stuff
sdiff_full = soup.find(id="sdiff-full")

# and these are the <tr> tags in that object with the xml we want
sdiff_xml = sdiff_full.find("tr", {"class" : ["sdiff-unc", "sdiff-add","sdiff-chg"]})


print sdiff_xml


# class sdiff-a: all of the "before" xml
# class sdiff-b: all of the "after" xml

# opening tags have class="sdl(some#) sds"
# closing tags have class="sdl(same#) sdz"
# text inside those tags has class="sdl(same#)"


# use regex to find all classes with sdl in the name... within the 
# "sdiff-full" thing... 