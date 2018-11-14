# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import pymongo
mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_auth = mongodb_client.admin
# db_auth.authenticate("root", "nju2019")
mongodb = mongodb_client["bug_report"]
mongodb_collection = mongodb["eclipse_platform"]
logger = logging.getLogger()


class EclipsePlatform(scrapy.Spider):
    name = "EclipsePlatform_EclipseBugzilla"
    start_urls = [
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=2000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=4000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=6000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=8000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=10000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=12000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=14000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=16000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=18000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=20000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=22000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=24000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=26000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=28000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=30000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=32000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=34000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=36000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=38000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=40000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=42000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=44000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=46000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=48000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=50000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=52000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=54000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=56000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=58000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=60000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=62000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=64000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=66000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=68000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=70000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=72000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=74000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=76000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=78000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=80000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=82000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=84000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=86000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=88000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=90000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=92000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=94000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=Platform&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=96000',
    ]

    def parse(self, response):
        response_data_json = response.css('pre::text').extract()[0]
        response_data_json.replace("\n", "")
        response_data_object = json.loads(response_data_json)
        bug_reports = response_data_object.get('bugs')
        mongodb_collection.insert_many(bug_reports)
        logger.info('Insert bug report in ' + response.url + ' complete.')
        for bug_report in bug_reports:
            bug_report_id = bug_report.get('id')
            yield scrapy.Request('https://bugs.eclipse.org/bugs/rest/bug/' + str(bug_report_id) + '/comment',
                                 callback=self.comment_parse)

    def comment_parse(self, response):
        comments_response_data_json = response.css('pre::text').extract()[0]
        comments_response_data_json.replace("\n", "")
        comments_response_data_object = json.loads(comments_response_data_json)
        for bugs in comments_response_data_object:
            if bugs != "comments":
                for bug_report_id in comments_response_data_object[bugs]:
                    for comments in comments_response_data_object[bugs][bug_report_id]:
                        result = mongodb_collection.update({'id': int(bug_report_id)}, {'$set': {'comments':
                                                        comments_response_data_object[bugs][bug_report_id][comments]}})
                        logger.info('Comments of id = ' + str(bug_report_id) + ' updated.' + str(result))
