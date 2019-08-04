#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-08-03 15:25:12
# Project: news_qq

from pyspider.libs.base_handler import *
import re
import pymysql
import pymongo

# 文章正则
pattern_finance = re.compile('^(http|https)://finance.*')
pattern_artical = re.compile('^(http|https)://(.*?)-\d{8}.html(.*)')
pattern_pub_time = re.compile('\d{4}年\d{2}月\d{2}日\d{2}:\d{2}')


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://finance.people.com.cn/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_finance, each.attr.href):
                if re.match(pattern_artical, each.attr.href):
                    self.crawl(each.attr.href, callback=self.detail_page)
                else:
                    self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        pub_time = response.doc('.text_title > .box01 > .fl').text()
        pub_ret = re.search(pattern_pub_time, pub_time)
        if pub_ret is None:
            return
        url = response.url
        title = response.doc('.text_title > h1').text()
        content = response.doc('.text_con').html()
        text = response.doc('.text_con').text()
        publish_time = pub_ret.group()

        # 保存到mysql
        # self.save_to_mysql((title, text, url, publish_time))

        result = {
            "url": url,
            "title": title,
            "publish_time": publish_time,
            "content": content,
            "text": text,
        }
        # 保存到mongo
        self.save_to_mongo(result)
        return result

    # 保存到mysql
    def save_to_mysql(self, params):
        db = pymysql.connect(host='localhost', user='root', password='password', port=3306, db='spider')
        cursor = db.cursor()
        sql = 'INSERT INTO news_qq(title, content, url, pub_time) values(%s, %s, %s, %s)'
        try:
            cursor.execute(sql, params)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()

    # 保存到mongo
    def save_to_mongo(self, params):
        # 客户端连接
        client = pymongo.MongoClient('mongodb://user:password@localhost:27017')
        # 获取数据库
        db = client.spider
        # 获取集合
        collection = db.news_sql
        # 插入数据
        collection.insert(params)
