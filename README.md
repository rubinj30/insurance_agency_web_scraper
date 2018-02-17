# Web Scraper

## Backstory
This was my first attempt to create a web scraper, which extracts large amounts of data from websites. I built it for a self-directed side-project at work with the intention of collecting the contact info for Nationwide insurance agents around the country for cold-calling lists. These lists were normally paid for upfront by my company's marketing department, but I had a very basic understanding of what web scrapers were and I thought I would take a crack at building one with my budding Python skills. 

## Libraries
### requests
Allows you to make HTTP requests
### BeautifulSoup
Used for parsing through large amounts of XML data
### csv
Used to write to a .csv file that could be uploaded to an automated dialer

## Challenges
Some challenges included:
- my unfamiliarity (at the time of the project) with HTML and CSS, which made it more difficult to identify and grab the correct pieces of information
- I started this right around the time I was starting to realize that it might be best to change over from writing scripts to leveraging functions and functional programming. This was difficult to run efficiently before I transitioned to using more functions
- A change was made to the HTML structure of Nationwide's site in the time I was working on this, so I had to refactor to make sure it was correctly obtaining data
- Code smell: In self-teaching, I didn't realize how unclean code could cause problems until this project, but I eventually cleaned up all the code and it ended up being very beneficial
