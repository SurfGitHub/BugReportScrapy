# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import pymongo

mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_auth = mongodb_client.admin
# db_auth.authenticate("root", "nju2019")
mongodb = mongodb_client["bug_report"]
mongodb_collection = mongodb["firefox"]
logger = logging.getLogger()
urls = ['https://bugzilla.mozilla.org/rest/bug?product=Firefox&status=RESOLVED&status=VERIFIED&status=CLOSED']
for i in range(1, 77):
    urls.append(
        'https://bugzilla.mozilla.org/rest/bug?product=Firefox&status=RESOLVED&status=VERIFIED&status=CLOSED&limit=2000&offset=' + str(2000 * i))


class Firefox(scrapy.Spider):
    name = "Firefox_MozillaBugzilla"
    start_urls = urls

    def parse(self, response):
        response_data_json = response.body
        response_data_object = json.loads(response_data_json)
        bug_reports = response_data_object.get('bugs')
        mongodb_collection.insert_many(bug_reports)
        logger.info('Insert bug report in ' + response.url + ' complete.')
        for bug_report in bug_reports:
            bug_report_id = bug_report.get('id')
            yield scrapy.Request('https://bugzilla.mozilla.org/rest/bug/' + str(bug_report_id) + '/comment',
                                 callback=self.comment_parse)

    def comment_parse(self, response):
        comments_response_data_json = response.body
        comments_response_data_object = json.loads(comments_response_data_json)
        for bugs in comments_response_data_object:
            if bugs != "comments":
                for bug_report_id in comments_response_data_object[bugs]:
                    for comments in comments_response_data_object[bugs][bug_report_id]:
                        result = mongodb_collection.update({'id': int(bug_report_id)}, {'$set': {'comments':
                                                                                                     comments_response_data_object[
                                                                                                         bugs][
                                                                                                         bug_report_id][
                                                                                                         comments]}})
                        logger.info('Comments of id = ' + str(bug_report_id) + ' updated.' + str(result))
