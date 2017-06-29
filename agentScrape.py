# works temp and packages each list together

import openpyxl as xl
import webbrowser
import requests
import bs4
import time
import pandas as pd

agentContactInfo = []

#currently testing Ohio
stateAbbrev = 'oh'

#currently manually entering list of cities
cities = ['akron','canton','cincinnati','cleveland','columbus','toledo','dayton','youngstown']
agentContactInfo = []
cityOhParsedList = []

#loop thru cities in list
for city in cities:
	siteWithCity = 'http://agent.franchiseSite.com/' + city + '-oh?page='
	# need to incorporate a variable for amount of pages
	
	#loop thru pages of each city
	for page in range(1,3):
        CityOh = requests.get(siteWithCity + str(page))
        soupCityOh = bs4.BeautifulSoup(cityOh.content, 'html.parser')
		officeNameList = list(soupCityOh.find_all('h3', itemprop="name"))
		officeTelephone = soupCityOh.find_all('strong', itemprop="telephone")
		streetAddressList = soupCityOh.find_all('div', itemprop="streetAddress")
		addressLocalityList = soupCityOh.find_all('span', itemprop="addressLocality")
		addressRegionList = soupCityOh.find_all('span', itemprop="addressRegion")
		postalCodeList = soupCityOh.find_all('span', itemprop="postalCode")
		
		time.sleep(5)
		for office, number, street, city, state, code in zip(officeNameList, officeTelephone, streetAddressList, addressLocalityList, addressRegionList, postalCodeList):
            		agentContactInfo.append(office.getText())
			agentContactInfo.append(number.getText())
			agentContactInfo.append(street.getText())
			agentContactInfo.append(city.getText())
			agentContactInfo.append(state.getText())
			agentContactInfo.append(code.getText())
			
			#append each agent's contact info and then clear list and grab next agent's info to append and so on
			cityOhParsedList.append(agentContactInfo)
			agentContactInfo = []

pd.DataFrame(cityOhParsedList).to_csv('scrape-' + stateAbbrev +'.csv')
