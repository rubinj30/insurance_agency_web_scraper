import openpyxl as xl
import webbrowser
import requests
import bs4
import time
import pandas as pd


#currently testing Ohio
state2 = 'oh'

#currently manually entering list of cities
cities = ['akron','canton']#,'cincinnati']#,'cleveland','columbus','toledo','dayton','findlay','toledo','youngstown']

# Blank list used to create list and list of lists, which will eventually be put into dataframe
allAgentContactInfo = []
agentContactInfo = []

#loop thru cities in list
for city in cities:
	siteWithCity = 'http://agency.nationwide.com/' + city + '-oh?page='

	#loop thru pages of each city
	for page in range(1,10):
		citiesRequest = requests.get(siteWithCity + str(page))
		citiesBs = bs4.BeautifulSoup(citiesRequest.content, 'html.parser')
		officeNameList = list(citiesBs.find_all('span', itemprop="name"))
		officeNameList2 = citiesBs.find_all('span', itemprop="name")
		officeTelephone = citiesBs.find_all('strong', itemprop="telephone")
		streetAddressList = citiesBs.find_all('div', itemprop="streetAddress")
		addressLocalityList = citiesBs.find_all('span', itemprop="addressLocality")
		addressRegionList = citiesBs.find_all('span', itemprop="addressRegion")
		postalCodeList = citiesBs.find_all('span', itemprop="postalCode")
		time.sleep(4)


		for name, name2, telephone, address, locality, state, zipCode in zip(officeNameList2[::2], officeNameList2[1::2], officeTelephone, streetAddressList, addressLocalityList, addressRegionList, postalCodeList):
			#had to adjust the tags and find way to remove \n's
			agentContactInfo.append(str(name.getText()).replace('\n',''))
			
			#adding office name
			agentContactInfo.append(name2.getText())
			agentContactInfo.append(telephone.getText())
			agentContactInfo.append(address.getText())
			agentContactInfo.append(locality.getText())
			agentContactInfo.append(state.getText())
			agentContactInfo.append(zipCode.getText())
			
			#append each agent's info to the list of lists and then clear for next agent
			allAgentContactInfo.append(agentContactInfo)
			agentContactInfo = []

print(allAgentContactInfo)
pd.DataFrame(allAgentContactInfo).to_csv('scrapeOh11.csv')
