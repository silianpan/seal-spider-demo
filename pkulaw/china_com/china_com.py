#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    :
# @File    : china_com_cn.py
# @Software: PyCharm

import requests
import pymysql

from fake_useragent import UserAgent
from pyquery import PyQuery as pq
from pyspider.libs.base_handler import *

start_url = 'http://www.china.com.cn/law/flfg/node_7001451.htm'


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
        self.crawl(start_url, user_agent=UserAgent().random, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        menu_title_list = response.doc('a.font2').items()
        for menu_title in menu_title_list:
            menu_text = menu_title.text()
            menu_href = menu_title.attr('href')
            if u'更多>>' == menu_text and 'node_7001457.htm' not in menu_href:
                self.crawl(menu_href, user_agent=UserAgent().random, callback=self.item_page)

    def item_page(self, response):
        news_list = response.doc('.unnamed6').items()
        for news in news_list:
            news_href = news.attr('href')
            news_title = news.text()
            self.crawl(news_href, user_agent=UserAgent().random, callback=self.detail_page, save={'title': news_title})
        # 下一页
        next_list = response.doc('#autopage > center > a').items()
        for next_page in next_list:
            next_href = next_page.attr('href')
            self.crawl(next_href, user_agent=UserAgent().random, callback=self.item_page)

    # 递归获取全部文章内容
    def all_next_content(self, next_href, all_content=[]):
        # 请求当前页
        ret = requests.get(next_href)
        mydoc = pq(ret.content)
        # 添加内容到列表
        con = mydoc('#fontzoom').html().strip()
        all_content.append(con)
        # 请求下一页
        next_mydoc = pq(mydoc('#autopage').html())
        npage = next_mydoc('a:last')
        if npage:
            npage_text = npage.text()
            if npage_text == u'下一页':
                npage_href = next_href[:next_href.rindex('/')+1] + npage.attr('href')
                self.all_next_content(npage_href, all_content)

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('#fontzoom').html().strip()
        all_content = [content]
        next_page = response.doc('#autopage > center > a:last-child')
        if next_page and u'下一页' == next_page.text():
            self.all_next_content(next_page.attr('href'), all_content)
        ret = {
            "url": response.url,
            "title": response.save.get('title', ''),
            "content": ''.join(all_content),
            "remark": 'http://www.china.com.cn/law/flfg/node_7001451.htm'
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
