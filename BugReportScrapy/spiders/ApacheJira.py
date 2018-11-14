# -*- coding: utf-8 -*-
import scrapy
import logging
import pymongo
import csv
import xmltodict
mongodb_client = pymongo.MongoClient("mongodb://47.101.47.191:27017/")
db_auth = mongodb_client.admin
db_auth.authenticate("root", "nju2019")
mongodb = mongodb_client["bug_report"]
mongodb_collection = mongodb["tomcat7"]
logger = logging.getLogger()
urls = []
csv_file = csv.reader(
            open('C:\\Users\\Administrator\\Documents\\Document\\Master Document\\研毕设\\数据爬取\\xml\\tomcat7.csv', 'r',encoding='UTF-8'))
for bug_report in csv_file:
    if (bug_report[0] == 'Bug ID'):
        continue
    else:
        urls.append('https://bz.apache.org/bugzilla/show_bug.cgi?ctype=xml&id=' + bug_report[0])


class Apache_Bugzilla(scrapy.Spider):
    name = "Apache_Jira_1"
    start_urls = urls

    def parse(self, response):
        bug_report_xml = response.text
        bug_report_dict = xmltodict.parse(bug_report_xml)
        bug_dict = bug_report_dict.get('bugzilla').get('bug')
        mongodb_collection.insert(bug_dict)
        logging.info('Insert ' + str(response.url) + ' complete.')
