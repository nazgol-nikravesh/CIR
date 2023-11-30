import CIR

if __name__ == '__main__':
    crawled_data=[]
    for i in range(10550,10601):
        print(i)
        crawled_data.append(CIR.Crawl_issue_report('https://issues.apache.org/jira/browse/CAMEL-'+str(i), str(i)))
    CIR.Write_to_CSV(crawled_data, '10550_to_10600')