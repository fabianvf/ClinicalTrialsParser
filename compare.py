import requests
import json
from bs4 import BeautifulSoup

py = requests.get("http://api.lillycoi.com/v1/trials.json?offset=20&limit=100");
data = py.text

soup = BeautifulSoup(data)

print(soup.prettify())
