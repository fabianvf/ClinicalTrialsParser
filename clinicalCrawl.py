import requests
from bs4 import BeautifulSoup

req = requests.get("http://clinicaltrials.gov/ct2/about-site/crawling")
data = req.text
soup = BeautifulSoup(data)

linklist=[]

for link in soup.find_all('a'):
	valid_link = link.get('href')
	if(valid_link[0:11]=="/ct2/crawl/"):
		linklist.append(valid_link)

trial_id_list=[]
id_file=open("nct_id_list.txt", 'w')

for group in linklist:
	req2 = requests.get("http://clinicaltrials.gov"+group)
	soup2=BeautifulSoup(req2.text)
	for link in soup2.find_all('a'):
		valid_link= link.get('href')
		if(valid_link[0:10]=="/ct2/show/"):
			nct_id=valid_link[10:]
			print valid_link[10:] 
			id_file.write(repr(nct_id)+"\n")

id_file.close()


