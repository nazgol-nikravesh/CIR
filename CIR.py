import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def Crawl_issue_report(url, issue_num):
    # Fetch the issue report
    response = requests.get(url)

    if response.status_code == 200:
        # Parsing the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')


        # Extracting Details
        issue_type_element = soup.select_one('span[id="type-val"]')
        issue_type = issue_type_element.text.strip().replace('"', '') if issue_type_element else None

        issue_status_element = soup.select_one('span[id="status-val"]')
        issue_status = issue_status_element.text.strip().replace('"', '') if issue_status_element else None

        issue_priority_element = soup.select_one('span[id="priority-val"]')
        issue_priority = issue_priority_element.text.strip().replace('"', '') if issue_priority_element else None

        issue_resolution_element = soup.select_one('span[id="resolution-val"]')
        issue_resolution = issue_resolution_element.text.strip().replace('"', '') if issue_resolution_element else None

        issue_affects_version_element = soup.select_one('span[id="versions-field"]')
        issue_affects_version = issue_affects_version_element.text.strip().replace('"', '') if issue_affects_version_element else None

        issue_fix_version_element = soup.select_one('span[id="fixVersions-field"]')
        issue_fix_version = issue_fix_version_element.text.strip().replace('"','') if issue_fix_version_element else None

        issue_component_element = soup.select_one('span[id="components-val"]')
        issue_component = issue_component_element.text.strip().replace('"', '') if issue_component_element else None

        issue_labels_element = soup.select_one('div[class="labels-wrap value"]')
        issue_labels = issue_labels_element.text.strip().replace('"', '') if issue_labels_element else None

        issue_estimated_complexity_element = soup.select_one('div[class ="value type-select"]')
        issue_estimated_complexity = issue_estimated_complexity_element.text.strip().replace('"', '') if issue_estimated_complexity_element else None

        # Extracting People
        assignee_element = soup.select_one('span[id="assignee-val"]')
        assignee = assignee_element.text.strip().replace('"', '') if assignee_element else None

        reporter_element = soup.select_one('span[id="reporter-val"]')
        reporter = reporter_element.text.strip().replace('"', '') if reporter_element else None

        votes_element = soup.select_one('aui-badge[id="vote-data"]')
        votes = votes_element.text.strip().replace('"', '') if votes_element else None

        watchers_element = soup.select_one('aui-badge[id="watcher-data"]')
        watchers = watchers_element.text.strip().replace('"', '') if watchers_element else None

        # Extracting Date
        created_element = soup.select_one('span[id="created-val"]')
        created = created_element.text.strip().replace('"', '') if created_element else None

        updated_element = soup.select_one('span[id="updated-val"]')
        updated = updated_element.text.strip().replace('"', '') if updated_element else None

        resolved_element = soup.select_one('span[id="resolutiondate-val"]')
        resolved = resolved_element.text.strip().replace('"', '') if resolved_element else None

        # Extracting Description
        description_element = soup.select_one('div[id="description-val"]')
        description = description_element.text if description_element else None

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

        comments_element = soup_comment.select_one('div[id="issue_actions_container"]')
        comments = comments_element.text if comments_element else None


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



