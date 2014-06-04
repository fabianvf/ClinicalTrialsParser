import requests
import json
from bs4 import BeautifulSoup

class CT_App(object):
	def __init__(self,id):
		self.id = id
		self.tab =  requests.get('https://clinicaltrials.gov/ct2/show/record/' + id)
		self.full = requests.get('https://clinicaltrials.gov/ct2/show/study/' + id)
		self.results = requests.get('https://clinicaltrials.gov/ct2/show/results/' + id)
	def html_to_txt(self, view):
		str_name = view
		if view == 'tab':
			view = self.tab
		elif view == 'full':
			view = self.full
		elif view == 'results':
			view = self.results
		else:
			print 'not valid view name' 
		with open(('CT_'+ str_name +'_'+self.id+'.html'), 'w') as htmltxt:
			htmltxt.write(view.text.encode('utf-8'))
		

#soupfull = BeautifulSoup(CT_API_fulltext.text).get_text().encode('utf-8')
#souptab = BeautifulSoup(CT_API_tab.text).get_text().encode('utf-8')
#soupstudy = BeautifulSoup(CT_API_Study.text).get_text().encode('utf-8')


#testCTApp = CT_App('NCT00936455')
#testCTApp.html_to_txt('tab')
#testCTApp.html_to_txt('results')
#testCTApp.html_to_txt('full')

#x = requests.get('http://clinicaltrials.gov/search?term=acne&displayxml=true')
#with open('seeXMLresults.txt', 'w') as xml_text:
#	xml_text.write(x.text.encode('utf-8'))