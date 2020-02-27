#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    : 
# @File    : china_law.py
# @Software: PyCharm

import pymysql

from pyspider.libs.base_handler import *

start_url = 'http://www.chinalaw.gov.cn/Department/node_592.html'


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw_other')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        menu_title_list = response.doc('.menuTitle > dl > a').items()
        for menu_title in menu_title_list:
            menu_href = menu_title.attr('href')
            json_url = 'http://www.chinalaw.gov.cn/json/' + menu_href[-8:-5] + '_1.json'
            self.crawl(json_url, callback=self.item_page)

        menu_content_list = response.doc('.menuContent > li > a').items()
        for menu_content in menu_content_list:
            menu_content_href = menu_content.attr('href')
            json_url = 'http://www.chinalaw.gov.cn/json/' + menu_content_href[-8:-5] + '_1.json'
            self.crawl(json_url, callback=self.item_page)

    def item_page(self, response):
        # news_list = response.doc('.news_list > ul > li').items()
        # for news in news_list:
        #     pub_date = news('dd').text()
        #     news_href = news('dt > a').attr('href')
        #     news_title = news('dt > a').text()
        #     self.crawl(news_href, callback=self.detail_page, save={'pub_date': pub_date, 'title': news_title})
        res_json = response.json
        for json_item in res_json:
            title = json_item.get('listtitle')
            pub_date = json_item.get('releasedate')
            news_href = 'http://www.chinalaw.gov.cn' + json_item.get('infostaticurl')
            self.crawl(news_href, callback=self.detail_page, save={'pub_date': pub_date, 'title': title})

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('#content > span').html()
        if content:
            ret = {
                "url": response.url,
                "title": response.save.get('title', ''),
                "pub_date": response.save.get('pub_date', ''),
                "content": content.strip(),
                "remark": 'http://www.chinalaw.gov.cn'
            }
            self.save_to_mysql(ret)
            return ret

    # 保存到mysql
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO law(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline, appr_dept, appr_date, remark) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('title', ''), ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('law_type', ''), ret.get('force_level', ''),
                ret.get('time_valid', ''), ret.get('impl_date', ''), ret.get('content', ''), ret.get('url', ''),
                ret.get('type', ''), ret.get('deadline', ''),
                ret.get('appr_dept', ''),
                ret.get('appr_date', ''),
                ret.get('remark', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')

