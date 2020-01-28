#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-14 15:19:11
# Project: pkulaw

import re

import pymysql
from pyspider.libs.base_handler import *

# 正则表达式
pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Origin': 'http://www.pkulaw.cn',
            'Referer': 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&',
            'Host': 'www.pkulaw.cn',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    @every(minutes=10 * 24 * 60)
    def on_start(self):
        # 第一页请求抓取
        self.crawl('http://www.pkulaw.cn/doSearch.ashx', method='POST', data={
            'Db': 'chl',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXA01',
            'clust_db': 'chl',
            'range': 'name',
            'menu_item': 'law'
        }, callback=self.index_page)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        pages = response.doc('.main-top4-1 > table > tr:first-child > td > span').text()
        pages_ret = re.match(pattern_page, pages)
        if pages_ret:
            current_index = int(pages_ret.group(1))
            page_size = int(pages_ret.group(2))
            if 1 < current_index <= page_size:
                # 回调index_page
                self.crawl('http://www.pkulaw.cn/doSearch.ashx', method='POST', data={
                    'range': 'name',
                    'check_hide_xljb': 1,
                    'Db': 'chl',
                    'check_gaojijs': 1,
                    'orderby': '%E5%8F%91%E5%B8%83%E6%97%A5%E6%9C%9F',
                    'hidtrsWhere': '377EF8C056C62113E3510356CD866D062CD82F4BD0A1F26B',
                    'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXA01',
                    'aim_page': current_index - 1,
                    'page_count': page_size,
                    'clust_db': 'chl',
                    'menu_item': 'law'
                }, callback=self.index_page)
        # 逐条处理
        self.item_page(response)

    @config(priority=2)
    def item_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if each.attr['class'] == 'main-ljwenzi' and re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)

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
        if u'现行有效' in ret['time_valid'] or u'尚未生效' in ret['time_valid']:
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
