# -*- coding: utf-8 -*-
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
mongodb_collection = mongodb["hibernate"]
logger = logging.getLogger()

hibernate_baseurl = "https://hibernate.atlassian.net/rest/api/3/search"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Bearer": "<access_token>"
}
hibernate_urls = []
for i in range(65, 66):
    payload = json.dumps({
        "jql": "project = HHH & status in (Resolved, Closed) & issuetype = Bug",
        "startAt": i * 100,
        "maxResults": 100,
        "fields": [
            "summary",
        ],
    })
    response = requests.request(
        "POST",
        hibernate_baseurl,
        data=payload,
        headers=headers
    )
    response_object = json.loads(response.text)
    for issue in response_object.get('issues'):
        hibernate_urls.append(
            "https://hibernate.atlassian.net/si/jira.issueviews:issue-xml/" + issue.get('key') + "/" + issue.get(
                'key') + ".xml")


class Hibernate_Jira(scrapy.Spider):
    name = "Hibernate_Jira"
    start_urls = hibernate_urls

    def parse(self, response):
        bug_report_xml = response.text
        bug_report_dict = xmltodict.parse(bug_report_xml)
        bug_dict = bug_report_dict.get('rss').get('channel').get('item')
        mongodb_collection.insert(bug_dict)
        logging.info('Insert ' + str(response.url) + ' complete.')
