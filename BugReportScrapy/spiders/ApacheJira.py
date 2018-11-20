# -*- coding: utf-8 -*-
#需要修改项目名、数据库名、range的范围
import scrapy
import logging
import pymongo
import xmltodict
import requests
import json

mongodb_client = pymongo.MongoClient("mongodb://47.101.47.191:27017/")
db_auth = mongodb_client.admin
db_auth.authenticate("root", "nju2019")
mongodb = mongodb_client["bug_report"]
mongodb_collection = mongodb["derby"]
logger = logging.getLogger()

apache_jira_baseurl = "https://issues.apache.org/jira/rest/api/2/search"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Bearer": "<access_token>"
}
apache_jira_urls = []
for i in range(35, 36):
    payload = json.dumps({
        "jql": "project = Derby & status in (Resolved, Closed) & issuetype = Bug",
        "startAt": i * 100,
        "maxResults": 100,
        "fields": [
            "summary",
        ],
    })
    response = requests.request(
        "POST",
        apache_jira_baseurl,
        data=payload,
        headers=headers
    )
    response_object = json.loads(response.text)
    for issue in response_object.get('issues'):
        apache_jira_urls.append(
            "https://issues.apache.org/jira/si/jira.issueviews:issue-xml/" + issue.get('key') + "/" + issue.get(
                'key') + ".xml")


class Apache_Jira(scrapy.Spider):
    name = "Apache_Jira"
    start_urls = apache_jira_urls

    def parse(self, response):
        bug_report_xml = response.text
        bug_report_dict = xmltodict.parse(bug_report_xml)
        bug_dict = bug_report_dict.get('rss').get('channel').get('item')
        mongodb_collection.insert(bug_dict)
        logging.info('Insert ' + str(response.url) + ' complete.')
