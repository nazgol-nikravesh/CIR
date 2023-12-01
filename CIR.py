import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def Extract(sp, elmnt, strip=1, omit_double_qout=1):
    # Issue properties extracting function
    element = sp.select_one(elmnt)
    if strip!=1 and omit_double_qout!=1:
        issue_prop = element.text if element else None
    elif strip!=1 and omit_double_qout==1:
        issue_prop = element.text.replace('"', '') if element else None
    elif strip==1 and omit_double_qout!=1:
        issue_prop = element.text.strip() if element else None
    else:
        issue_prop = element.text.strip().replace('"', '') if element else None
    return issue_prop
def Crawl_issue_report(url, issue_num):
    # Fetching the issue report
    response = requests.get(url)

    if response.status_code == 200:
        # Parsing the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')


        # Extracting Details
        issue_type = Extract(soup, 'span[id="type-val"]')
        issue_status = Extract(soup, 'span[id="status-val"]')
        issue_priority = Extract(soup, 'span[id="priority-val"]')
        issue_resolution = Extract(soup, 'span[id="resolution-val"]')
        issue_affects_version = Extract(soup, 'span[id="versions-field"]')
        issue_fix_version = Extract(soup, 'span[id="fixVersions-field"]')
        issue_component = Extract(soup, 'span[id="components-val"]')
        issue_labels = Extract(soup, 'div[class="labels-wrap value"]')
        issue_estimated_complexity = Extract(soup, 'div[class ="value type-select"]')

        # Extracting People
        assignee = Extract(soup, 'span[id="assignee-val"]')
        reporter = Extract(soup, 'span[id="reporter-val"]')
        votes = Extract(soup, 'aui-badge[id="vote-data"]')
        watchers = Extract(soup, 'aui-badge[id="watcher-data"]')

        # Extracting Date
        created = Extract(soup, 'span[id="created-val"]')
        updated = Extract(soup, 'span[id="updated-val"]')
        resolved = Extract(soup, 'span[id="resolutiondate-val"]')

        # Extracting Description
        description = Extract(soup, 'div[id="description-val"]', 0, 0)

        # Extracting Comments
        for scr in soup.findAll("script"):
            if 'comment-tabpanel' in scr.text:
                options = Options()
                options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
                options.add_argument('--disable-gpu')  # Disable GPU acceleration
                driver = webdriver.Chrome(options=options)
                # Navigate to the URL
                driver.get(url)
                # Execute JavaScript code
                result = driver.execute_script(scr.text)
                html_comment = driver.page_source

        soup_comment = BeautifulSoup(html_comment, 'html.parser')
        comments = Extract(soup_comment, 'div[id="issue_actions_container"]', 0, 0)

        crawled_data={
                'Issue#': issue_num,

                'Type': issue_type,  # Details Start
                'Status': issue_status,
                'Priority': issue_priority,
                'Resolution': issue_resolution,
                'Affects Version/s': issue_affects_version,
                'Fix Version/s': issue_fix_version,
                'Component/s': issue_component,
                'Labels': issue_labels,
                'Estimated Complexity': issue_estimated_complexity,  # Details End

                'Assignee': assignee,  # People Start
                'Reporter': reporter,
                'Number of Votes': votes,
                'Number of Watchers': watchers,  # People End

                'Created': created,  # Dates Start
                'Updated': updated,
                'Resolved': resolved,  # Dates End

                'Description': description,
                'Comments': comments
            }

        return crawled_data

    else:
        return None
def Write_to_CSV(data,CSV_name):
        if data:
            # Write to CSV
            with open(CSV_name+'_issue_report.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Issue#','Type', 'Status', 'Priority', 'Resolution', 'Affects Version/s', 'Fix Version/s', 'Component/s', 'Labels','Estimated Complexity',
     'Assignee','Reporter', 'Number of Votes', 'Number of Watchers', 'Created', 'Updated', 'Resolved', 'Description', 'Comments']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)



                # Write header
                writer.writeheader()
                for raw in data:
                    # Write data
                    writer.writerow(raw)
            print("CSV file generated successfully.")
        else:
            print(f"Failed to fetch webpage.")



