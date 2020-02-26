#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    : 
# @File    : china_law.py
# @Software: PyCharm

import pymysql

from pyspider.libs.base_handler import *

start_url = 'http://search.chinalaw.gov.cn/AdvanceSearchResult?SiteID=124&PageIndex=&c1=1900-01-01&c2=3000-01-01&c3=&c4=&title=&Query='


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
        next_item_all = response.doc('.pagebar > a').items()
        for next_item in next_item_all:
            next_txt = next_item.text()
            if next_txt == u'下一页':
                next_num = next_item.attr('page')
                next_url = 'http://search.chinalaw.gov.cn/AdvanceSearchResult?SiteID=124&PageIndex=' + str(next_num) + '&c1=1900-01-01&c2=3000-01-01&c3=&c4=&title=&Query='
                self.crawl(next_url, callback=self.index_page)

        item_list = response.doc('.w_lt > a').items()
        for item in item_list:
            item_href = item.attr('href')
            self.crawl(item_href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        dinfor_list = response.doc('.d_infor > tr > td').items()
        i = 1
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
            "pub_date": pub_dept,
            "content": response.doc('.con').html().strip(),
            "remark": 'http://search.chinalaw.gov.cn',
            "pub_date": pub_date,
            "impl_date": impl_date,
            "time_valid": time_valid,
            "law_type": law_type
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
