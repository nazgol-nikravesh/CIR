import CIR

if __name__ == '__main__':
    crawled_data = CIR.Crawl_issue_report('https://issues.apache.org/jira/browse/CAMEL-10597', '10597')
    CIR.Write_to_CSV([crawled_data], 'example')