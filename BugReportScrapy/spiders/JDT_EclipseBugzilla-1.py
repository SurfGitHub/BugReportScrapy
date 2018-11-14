# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import pymongo
mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_auth = mongodb_client.admin
# db_auth.authenticate("root", "nju2019")
mongodb = mongodb_client["bug_report"]
mongodb_collection = mongodb["jdt"]
logger = logging.getLogger()


class JDT(scrapy.Spider):
    name = "JDT_EclipseBugzilla-1"
    start_urls = [
        'https://bugs.eclipse.org/bugs/rest/bug?product=JDT&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=48000',
        'https://bugs.eclipse.org/bugs/rest/bug?product=JDT&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=50000',
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
