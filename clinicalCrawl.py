import requests
from bs4 import BeautifulSoup

req = requests.get("http://clinicaltrials.gov/ct2/about-site/crawling")
data = req.text
soup = BeautifulSoup(data)

linklist=[]

for link in soup.find_all('a'):
	valid_link = link.get('href')
	linklist.append(valid_link)

wrapper_ind = linklist.index('#wrapper')
first_crawl_ind = linklist.index('/ct2/crawl/0')

del linklist[wrapper_ind:]
del linklist[:first_crawl_ind]

for group in linklist:
	req2 = requests.get("http://clinicaltrials.gov"+group)



print linklist
