# -*- coding:utf-8 -*-
import pymongo

# Per-Process for bug reports crawled from Apache Bugzilla
# variables need to be modified
# path of file generated by the algorithm
file_path = ''
# IP address and port of your Mongodb
mongodb_ip_port = '47.101.47.191:27017'
# username of mongodb(with admin privileges)
mongodb_username = 'root'
# password of mongodb_username
mongodb_password = 'nju2019'
# name of mongodb database contains the bug reports crawled from Apache Bugzilla
mongodb_database_name = 'bug_report'
# name of mongodb collection which you want to pre-process
mongodb_collection_name = 'tomcat5'

mongodb_client = pymongo.MongoClient('mongodb://' + mongodb_ip_port + '/')
db_auth = mongodb_client.admin
db_auth.authenticate(mongodb_username, mongodb_password)
mongodb = mongodb_client[mongodb_database_name]
mongodb_collection = mongodb[mongodb_collection_name]

file = open(file_path)
line = file.readline()

while line:
