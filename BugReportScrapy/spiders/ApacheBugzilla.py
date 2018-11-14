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
mongodb_collection = mongodb["ant"]
logger = logging.getLogger()


class JDT(scrapy.Spider):
    name = "Apache_Bugzilla"
    start_urls = [
        'https://bz.apache.org/bugzilla/show_bug.cgi?ctype=xml&id=57431',
    ]

    def parse(self, response):
        csv_file = csv.reader(
            open('C:\\Users\\Administrator\\Documents\\Document\\Master Document\\研毕设\\数据爬取\\xml\\ant.csv', 'r'))
        for bug_report in csv_file:
            if (bug_report[0] == 'Bug ID'):
                continue
            else:
                yield scrapy.Request('https://bz.apache.org/bugzilla/show_bug.cgi?ctype=xml&id=' + bug_report[0],
                                     callback=self.bug_parse)

    def bug_parse(self, response):
        bug_report_xml = response.text
        bug_report_dict = xmltodict.parse(bug_report_xml)
        bug_dict = bug_report_dict.get('bugzilla').get('bug')
        mongodb_collection.insert(bug_dict)
        logging.info('Insert ' + str(response.url) + ' complete.')
