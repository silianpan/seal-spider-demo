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

start_url = 'http://search.chinalaw.gov.cn/AdvanceSearchResult?SiteID=124&PageIndex=&c1=1900-01-01&c2=3000-01-01&c3=&c4=&title=&Query='


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, user_agent=UserAgent().random, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        next_item_all = response.doc('.pagebar > a').items()
        for next_item in next_item_all:
            next_txt = next_item.text()
            if next_txt == u'下一页':
                next_num = next_item.attr('page')
                next_url = 'http://search.chinalaw.gov.cn/AdvanceSearchResult?SiteID=124&PageIndex=' + str(next_num) + '&c1=1900-01-01&c2=3000-01-01&c3=&c4=&title=&Query='
                self.crawl(next_url, user_agent=UserAgent().random, callback=self.index_page)

        item_list = response.doc('.w_lt > a').items()
        for item in item_list:
            item_href = item.attr('href')
            self.crawl(item_href, user_agent=UserAgent().random, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        dinfor_list = response.doc('.d_infor > tr > td').items()
        i = 0
        for dinfor in dinfor_list:
            if i == 1:
                pub_dept = dinfor.text()
            elif i == 3:
                pub_date = dinfor.text()
            elif i == 5:
                impl_date = dinfor.text()
            elif i == 7:
                time_valid = dinfor.text()
            elif i == 9:
                law_type = dinfor.text()
            i = i + 1

        ret = {
            "url": response.url,
            "title": response.doc('.conTit').text(),
            "pub_dept": pub_dept,
            "content": response.doc('.con').html().strip(),
            "remark": 'http://search.chinalaw.gov.cn',
            "pub_date": pub_date,
            "impl_date": impl_date,
            "time_valid": time_valid,
            "law_type": law_type
        }
        return ret

    def on_result(self, result):
        if result and result['title'] and result['content']:
            sql = MysqlUtil()
            sql.insert('law', **result)
