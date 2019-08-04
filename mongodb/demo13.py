#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-04 13:49
# @Author  : liupan
# @Site    : 
# @File    : demo13.py
# @Software: PyCharm

import pymongo

client = pymongo.MongoClient('mongodb://user:password@localhost:27017')
# 数据库
db = client['spider']
# 集合
collection = db['news_sql']

ret = collection.find({'title': {'$regex': '.*?房地产.*'}})
# print(ret)
for item in ret:
    print(item['title'])
