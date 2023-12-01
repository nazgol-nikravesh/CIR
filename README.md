# CIR: Crawling Issue Reports

# GGHRstatistics: Get GitHub Repository statistics
A crawler for parsing  and storing Jira issue reports

## .py files
### 1. Core file: CIR.py   
This file contains functions for extracting data from Jira issue reports. The key functions include:   
- **1) Extract(sp, elmnt, strip=1, omit_double_qout=1):** Extracts issue properties from the specified HTML element.  
- **Inputs:**  
  - sp: A BeautifulSoup object representing the parsed HTML content.
  - elmnt: The HTML element identifier (e.g., tag and/or class) to extract properties from.
  - strip (optional, default=1): If set to 1, it removes leading and trailing whitespaces from the extracted text.
  - omit_double_qout (optional, default=1): If set to 1, it removes double quotes from the extracted text.  

- **Output:**
  - issue_prop: Extracted issue property as a string. It could be None if the specified HTML element is not found.  

- **2) Crawl_issue_report(url, issue_num):** Fetches an issue report from the given URL and extracts relevant Details, People, Dates, Description, and Comments.
 - **Inputs:**  
  - url: The URL of the Jira issue report to fetch and scrape.
  - issue_num: The issue number associated with the Jira issue report.  
 - **Output:**
  - issue_prop: Extracted issue property as a string. It could be None if the specified HTML element is not found. 
  - crawled_data: A dictionary containing various details, people, dates, description, and comments extracted from the Jira issue report. The keys include:
    - Issue#
    - Details (e.g., Type, Status, Priority, etc.)
    - People (e.g., Assignee, Reporter, etc.)
    - Dates (e.g., Created, Updated, etc.)
    - Description
    - Comments
- **3) Write_to_CSV(data, CSV_name):** Writes the crawled data to a CSV file.  
 - **Inputs:**  
  - data: The crawled data, typically in the form of a list of dictionaries, where each dictionary represents the data for a single issue report.
  - CSV_name: The base name for the CSV file. 

 - **Output:**
  - If successful, the function generates a CSV file named [CSV_name]_issue_report.csv containing the crawled data. It prints a success message.
  - If unsuccessful (e.g., failed to fetch the webpage), it prints an error message.


### 2. main-BachCrawlingIssueReports.py   
This file demonstrates the use of CIR.py to crawl multiple Jira issue reports within a specified range and writes the data to a CSV file.

 **Output Example:**   


### 3. mainExample.py   
This file provides an example of how to use CIR.py to crawl a specific Jira issue report and writes the data to a CSV file.

 **Output Example:**  



 **note: run the second and the third files to get the .csv files** 


## Dependencies (Python libraries)
- requests
- bs4 (BeautifulSoup)
- selenium
- chrome driver (for headless browsing)



