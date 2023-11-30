import requests
from bs4 import BeautifulSoup
import csv

def Crawl_issue_report(url):
    # Fetch the issue report
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        print(soup.select_one('span[id="type-val"]').text)



# Example
Crawl_issue_report('https://issues.apache.org/jira/browse/CAMEL-10597')
