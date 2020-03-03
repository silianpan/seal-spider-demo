#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    : 
# @File    : china_law.py
# @Software: PyCharm

from fake_useragent import UserAgent
from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysql_util import MysqlUtil

start_url = 'http://www.chinalaw.gov.cn/Department/node_592.html'


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, user_agent=UserAgent().random, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        menu_title_list = response.doc('.menuTitle > dl > a').items()
        for menu_title in menu_title_list:
            menu_href = menu_title.attr('href')
            json_url = 'http://www.chinalaw.gov.cn/json/' + menu_href[-8:-5] + '_1.json'
            self.crawl(json_url, user_agent=UserAgent().random, callback=self.item_page)

        menu_content_list = response.doc('.menuContent > li > a').items()
        for menu_content in menu_content_list:
            menu_content_href = menu_content.attr('href')
            json_url = 'http://www.chinalaw.gov.cn/json/' + menu_content_href[-8:-5] + '_1.json'
            self.crawl(json_url, user_agent=UserAgent().random, callback=self.item_page)

    def item_page(self, response):
        # news_list = response.doc('.news_list > ul > li').items()
        # for news in news_list:
        #     pub_date = news('dd').text()
        #     news_href = news('dt > a').attr('href')
        #     news_title = news('dt > a').text()
        #     self.crawl(news_href, user_agent=UserAgent().random, callback=self.detail_page, save={'pub_date': pub_date, 'title': news_title})
        res_json = response.json
        for json_item in res_json:
            title = json_item.get('listtitle')
            pub_date = json_item.get('releasedate')
            news_href = 'http://www.chinalaw.gov.cn' + json_item.get('infostaticurl')
            self.crawl(news_href, user_agent=UserAgent().random, callback=self.detail_page, save={'pub_date': pub_date, 'title': title})

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
            return ret

    def on_result(self, result):
        if result and result['title'] and result['content']:
            sql = MysqlUtil()
            sql.insert('law', **result)
