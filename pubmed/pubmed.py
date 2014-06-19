#you need biopython to access this libary easily
from Bio import Entrez
from Bio import Medline
from bs4 import BeautifulSoup
import requests

BASE = 'http://www.ncbi.nlm.nih.gov/pubmed/'
Entrez.email = "contact@cos.io"

#Find PMID's for a specific search
def get_articles(search_term):
    num_results = 0
    handle = Entrez.egquery(term=search_term)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"]=="pubmed":
            num_results = row["Count"]
    handle = Entrez.esearch(db="pubmed", term=search_term, retmax=num_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]
    return id_list

#Get info once you have PMID
def get_info(pmid):
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline",
        retmode="text")
    records = Medline.parse(handle)
    for record in records:
        print("title:", record.get("TI", "?"))
        print("authors:", record.get("AU", "?"))
        print("source:", record.get("SO", "?"))
        print("abstract:", record.get("AB", "?"))
        print("publication type", record.get("PT", "?"))
        print("")

def get_page(pmid):
    return BASE + pmid
    #should probably put in a check to see if page exists

def get_full_text(page):
    html_response = requests.get(page)
    html = html_response.text
    soup = BeautifulSoup(html)
    section = soup.find("div", {"class":"icons portlet"})
    if section == None:
        return None
    section = section.find('a')
    link = section.get('href')
    return link


#Mini Tests
#print(get_articles("organ"))
#get_info('12657584')
get_full_text(get_page('1896168'))
