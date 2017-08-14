import requests
from bs4 import BeautifulSoup
import sys
import csv


cities = ['akron', 'canton', 'cincinnati', 'cleveland', 'columbus', 'dayton', 'kent', 'youngstown']
urls_list = []


def get_list_of_urls(state):

    for city in cities:
        for page in range(1, 8):
            url = "http://agency.nationwide.com/{0}-{1}?page={2}".format(city, state, page)
            urls_list.append(url)

    print("URL lists for {} generated.".format(state.upper()))
    return urls_list


def scrape_agency_info(urls_list):
    """Returns lists of lists for agent info for a single page"""
    agent_info_list = []
    # indiv_agent_info_list = []  <------ This was never used
    # page_of_agent_info = [] <----- Don't need this anymore

    for url in urls_list:
        print("Scraping: {}".format(url))
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

            # This was redundant, and creating an extra list
            # which is why your CSV was printing out in only 1 column
            # page_of_agent_info.append([name, telephone, address, city, state, zip_code])
            # agent_info_list.append(page_of_agent_info)
            # page_of_agent_info = []

            # Replace with just the 1 line below

            # .tile() returns string in Title Case
            # So we're not getting "JOEL C. RECHT", it's not perfect (like LLC will return Llc)
            # But IMO it looks better
            # zip_code[:5] returns only the first 5 characters of the zip code so you don't
            # have some 5 digit and some 9 digit zips. You may want 9 digit zips when they're
            # available, if so change this.
            agent_info_list.append([name.title(), telephone, address, city, state, zip_code[:5]])

    print("Scraping Completed.")

    return agent_info_list


def write_offices_to_csv(agencies):
    """Write *agent_info_list* to a csv file called 'football_players.csv'"""
    # with open("/Users/path/refactoredScrape.csv", "w") as nationwide_csv:
    print("Writing to CSV...")

    # I noticed the CSV had extra spaces between each line, I've ran into this before and knew
    # there was a fix, so I googled "csv.writerow() extra line" and found this solution on
    # StackOverflow:
    # https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
    with open("refactoredScrape.csv", "w", newline="") as nationwide_csv:
        writer = csv.writer(nationwide_csv)
        writer.writerow(['Name', 'Office Phone', 'Address', 'City', 'State', 'Zipcode'])
        for each_office in agencies:
            writer.writerow(each_office)


def main():
    """Main entry point for script"""
    get_list_of_urls("oh")
    agent_info_list = scrape_agency_info(urls_list)
    write_offices_to_csv(agent_info_list)
    print("Completed process successfully!")

if __name__ == '__main__':
    sys.exit(main())
