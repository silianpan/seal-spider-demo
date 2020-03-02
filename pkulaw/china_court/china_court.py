#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    : 
# @File    : china_court.py
# @Software: PyCharm

import pymysql

from pyspider.libs.base_handler import *

start_url = 'https://www.chinacourt.org/law.shtml'


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
        menu_title_list = response.doc('ul.biaoti > li > a').items()
        for menu_title in menu_title_list:
            menu_text = menu_title.text()
            menu_href = menu_title.attr('href')
            if u'中外条约' != menu_text and u'立法追踪' != menu_text:
                self.crawl(menu_href, callback=self.item_page)

    def item_page(self, response):
        news_list = response.doc('.law_list > ul > li').items()
        for news in news_list:
            news_href = news('.left > a').attr('href')
            pub_date = news('.right').text()
            self.crawl(news_href, callback=self.detail_page, save={'pub_date': pub_date})
        # 下一页
        next_list = response.doc('.paginationControl > a').items()
        for next_page in next_list:
            if u'下一页' == next_page.text():
                next_href = next_page.attr('href')
                self.crawl(next_href, callback=self.item_page)
                break

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.content_text > div,p[style="text-align:center;"]:lt(4) > strong').text()
        if not title:
            title = response.doc('.content_text > div,p[style="text-align: center;"]:lt(3) > strong').text()
        if not title:
            title = response.doc('.content_text > p[style="text-align:center;"]:lt(3) > strong').text()
        if not title:
            title = response.doc('.content_text > p[style="text-align: center;"]:lt(3) > strong').text()
        if not title:
            title = response.doc('.content_text > p:lt(3) > span > strong').text()
        if not title:
            title = response.doc('.MTitle').text()
        if not title:
            title = response.doc('.content_text > div,p[style="text-align:center;"]:lt(4)').text()
        if not title:
            title = response.doc('.content_text > p[align="center"] > strong').text()
        content = response.doc('.content_text').html().strip()
        ret = {
            "url": response.url,
            "title": title,
            "pub_date": response.save.get('pub_date', ''),
            "content": content,
            "remark": 'https://www.chinacourt.org/law.shtml'
        }
        stitle = response.doc('.STitle').html().strip()
        for sitem in stitle.split(r'<br />'):
            if sitem:
                ret_item_list = sitem.strip().split(u'】')
                if len(ret_item_list) == 2:
                    if u'发布单位' in ret_item_list[0]:
                        ret['pub_dept'] = ret_item_list[1].strip()
                    elif u'发布文号' in ret_item_list[0]:
                        ret['pub_no'] = ret_item_list[1].strip()
                    elif u'发布日期' in ret_item_list[0]:
                        ret['pub_date'] = ret_item_list[1].strip()
                    elif u'生效日期' in ret_item_list[0]:
                        ret['impl_date'] = ret_item_list[1].strip()
                    elif u'失效日期' in ret_item_list[0]:
                        ret['deadline'] = ret_item_list[1].strip()
                    elif u'所属类别' in ret_item_list[0]:
                        ret['law_type'] = ret_item_list[1].strip()
                    elif u'所属类别' in ret_item_list[0]:
                        ret['law_type'] = ret_item_list[1].strip()
        if title and content:
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
