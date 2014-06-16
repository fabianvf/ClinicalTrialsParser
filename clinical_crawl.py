import requests
from bs4 import BeautifulSoup

"""This script uses BeautifulSoup to scrape the links for all of the studies currently on clinicaltrials.gov off of 
a clinicaltrials.gov page for webcrawlers."""

def ClinicalCrawl():
    data = requests.get("http://clinicaltrials.gov/ct2/about-site/crawling").text
    crawl_page_soup = BeautifulSoup(data)

    trial_links=[]

    for link in crawl_page_soup.find_all('a'):
        valid_link = link.get('href')
        if(valid_link[0:11] == "/ct2/crawl/"):
            trial_links.append(valid_link)

    trial_id_list=[]
    id_file=open("nct_id_list.txt", 'w')

    for group in trial_links:
        data = requests.get("http://clinicaltrials.gov"+group).text
        link_soup = BeautifulSoup(data)
        for link in link_soup.find_all('a'):
            valid_link = link.get('href')
            if(valid_link[0:10] == "/ct2/show/"):
                nct_id = valid_link[10:]
                print nct_id
                id_file.write(repr(nct_id)+"\n")

    id_file.close()

ClinicalCrawl()
