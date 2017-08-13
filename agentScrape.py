import requests
from bs4 import BeautifulSoup
import sys
import csv
 
cities = ['akron', 'canton', 'cincinnati', 'cleveland', 'columbus', 'dayton', 'kent', 'youngstown']
urls_list = []
 
# URL = "http://agency.nationwide.com/{0}-{1}".format(city, state)
 
def get_list_of_urls(state):
 
    for city in cities:
        url = "http://agency.nationwide.com/{0}-{1}?".format(city, state)
        for page in range(1, 8):
            url_with_page = (url + "page=" + str(page))
            urls_list.append(url_with_page)
    return urls_list
 
def scrape_agency_info(urls_list):
    """Returns lists of lists for agent info for a single page"""
    agent_info_list = []
    indiv_agent_info_list = []
    page_of_agent_info = []
 
    for url in urls_list:
        # get html
        nationwide_request = requests.get(url)
        nationwide_bs = BeautifulSoup(nationwide_request.content, 'html.parser')
 
        # loop thru each office on page, remove html/css, and place item in list with all similar items from other offices
        office_name_list = [x.getText() for x in nationwide_bs.find_all("span", itemprop="name")]
        office_telephone_list = [x.getText() for x in nationwide_bs.find_all("strong", itemprop="telephone")]
        office_address_list = [x.getText() for x in nationwide_bs.find_all("div", itemprop="streetAddress")]
        office_city_list = [x.getText() for x in nationwide_bs.find_all("span", itemprop="addressLocality")]
        office_state_list = [x.getText() for x in nationwide_bs.find_all("span", itemprop="addressRegion")]
        office_zip_code_list = [x.getText() for x in nationwide_bs.find_all("span", itemprop="postalCode")]
     
        # loop thru each list of items and append to list for each individual office to match up with other info
        for name, telephone, address, city, state, zip_code in zip(office_name_list[1::2], office_telephone_list, office_address_list, office_city_list, office_state_list, office_zip_code_list):
            page_of_agent_info.append([name, telephone, address, city, state, zip_code])
            agent_info_list.append(page_of_agent_info)
            page_of_agent_info = []
 
    return agent_info_list
 
def write_offices_to_csv(agencies):
    """Write *agent_info_list* to a csv file called 'football_players.csv'"""
    with open("/Users/path/refactoredScrape.csv", "w") as nationwide_csv:
        writer = csv.writer(nationwide_csv)
        for each_office in agencies:
            writer.writerow(each_office)
 
def main():
    """Main entry point for script"""
    get_list_of_urls("oh")
    agent_info_list = scrape_agency_info(urls_list)
    write_offices_to_csv(agent_info_list)
 
if __name__ == '__main__':
    sys.exit(main())
