#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-14 15:19:11
# Project: pkulaw_chl_law_xc02 中央法规-行政法规

import re
import uuid
import requests

import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

# 正则表达式
pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')
fake_ua = UserAgent()

# 请求参数设置
clusterwhere = '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXC02'
db = 'chl'
menu_item = 'law'
referer = 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&'


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': fake_ua.random,
            'Origin': 'http://www.pkulaw.cn',
            'Referer': referer,
            'Host': 'www.pkulaw.cn',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        },
        'cookies': {
            'isCheck': 'ValidateSuccess_126',
            'codeCompare': 'OK_126'
        }
    }

    def __init__(self):
        self.custom_proxy = None

    def get_proxy(self):
        ret = requests.get('http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&pack=81985&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4').json()
        return ret.get('data')[0].get('ip')+':'+str(ret.get('data')[0].get('port'))

    @every(minutes=10 * 24 * 60)
    def on_start(self):
        self.custom_proxy = self.get_proxy()
        ua = UserAgent()
        # 第一页请求抓取
        self.crawl('http://www.pkulaw.cn/doSearch.ashx?_=1', method='POST', data={
            'Db': db,
            'clusterwhere': clusterwhere,
            'clust_db': db,
            'range': 'name',
            'menu_item': menu_item
        }, callback=self.index_page, user_agent=ua.random, proxy=self.custom_proxy)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        pages = response.doc('.main-top4-1 > table > tr:first-child > td > span').text()
        pages_ret = re.match(pattern_page, pages)
        if pages_ret:
            current_index = int(pages_ret.group(1))
            page_size = int(pages_ret.group(2))
            if 1 <= current_index <= page_size:
                # 回调index_page
                ua = UserAgent()
                self.crawl('http://www.pkulaw.cn/doSearch.ashx?_=' + str(uuid.uuid4()), method='POST', data={
                    'range': 'name',
                    'Db': db,
                    'clusterwhere': clusterwhere,
                    'aim_page': current_index,
                    'page_count': page_size,
                    'clust_db': db,
                    'menu_item': menu_item
                }, callback=self.index_page, user_agent=ua.random, proxy=self.custom_proxy)
        # 逐条处理
        self.item_page(response)

    @config(priority=2)
    def item_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if each.attr['class'] == 'main-ljwenzi' and re.match(pattern_article, each.attr.href):
                ua = UserAgent()
                self.crawl(each.attr.href, callback=self.detail_page, user_agent=ua.random, proxy=self.custom_proxy)

    @config(priority=3)
    def detail_page(self, response):
        # 详细处理
        title = response.doc('table#tbl_content_main > tr:first-child > td > span > strong')
        li_list = response.doc('table#tbl_content_main > tr').items()
        ret = {}
        for li in li_list:
            td_list = li('td').items()
            for td in td_list:
                strong = td('font').text()
                if strong is not None:
                    strong = strong.strip()
                    if u'发布部门' in strong:
                        ret['pub_dept'] = td('a').text().strip()
                    elif u'发文字号' in strong:
                        td.children().remove()
                        ret['pub_no'] = td.text().strip()
                    elif u'发布日期' in strong:
                        td.children().remove()
                        ret['pub_date'] = td.text().strip()
                    elif u'实施日期' in strong:
                        td.children().remove()
                        ret['impl_date'] = td.text().strip()
                    elif u'时效性' in strong:
                        ret['time_valid'] = td('a').text().strip()
                    elif u'效力级别' in strong:
                        ret['force_level'] = td('a').text().strip()
                    elif u'法规类别' in strong:
                        ret['law_type'] = td('a').text().strip()
                    elif u'类别' in strong:
                        ret['type'] = td('a').text().strip()
                    elif u'截止日期' in strong.strip():
                        td.children().remove()
                        ret['deadline'] = td.text().strip()

        ret['url'] = response.url
        ret['title'] = title.text().strip()
        ret['content'] = response.doc('.Content > #div_content').html().strip()

        # 保存mysql
        if (u'现行有效' in ret['time_valid'] or u'尚未生效' in ret['time_valid']) and (u'任免' not in ret['force_level'] and
                                                                               u'工作文件' not in ret[
                                                                                   'force_level'] and u'工作答复' not in
                                                                               ret['force_level']):
            if 'deadline' not in ret:
                ret['deadline'] = ''
            if 'type' not in ret:
                ret['type'] = ''
            if 'pub_no' not in ret:
                ret['pub_no'] = ''
            self.save_to_mysql(
                (ret['title'], ret['pub_dept'], ret['pub_no'], ret['pub_date'], ret['law_type'], ret['force_level'],
                 ret['time_valid'], ret['impl_date'], ret['content'], ret['url'], ret['type'], ret['deadline']))
        return ret

    # 保存到mysql
    def save_to_mysql(self, params):
        db = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw')
        cursor = db.cursor()
        sql = 'INSERT INTO law(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql, params)
            db.commit()
        except:
            db.rollback()
        # cursor.execute(sql, params)
        # db.commit()
        cursor.close()
        db.close()
