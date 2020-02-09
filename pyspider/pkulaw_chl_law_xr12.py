#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-14 15:19:11
# Project: pkulaw_chl_law_xr12 中央法规-党内法规

import json
import re

import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

# 正则表达式
pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')

# 请求参数设置
clusterwhere = '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXR12'
Db = 'chl'
clust_db = 'chl'
menu_item = 'law'
referer = 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&'

common_formdata = {
    'Db': Db,
    'clust_db': clust_db,
    'menu_item': menu_item,
    'range': 'name',
    'clusterwhere': clusterwhere
}

common_headers = {
    'Referer': referer,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.pkulaw.cn',
    'Origin': 'http://www.pkulaw.cn'
}
common_detail_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.pkulaw.cn',
    'Upgrade-Insecure-Requests': '1'
}


class Handler(BaseHandler):
    crawl_config = {
        'cookies': {
            'isCheck': 'ValidateSuccess_126',
            'codeCompare': 'OK_126'
        }
    }

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.pkulaw.cn/doSearch.ashx', method='POST', headers=common_headers, data=common_formdata,
                   callback=self.index_page,
                   user_agent=UserAgent().random)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        pages = response.doc('.main-top4-1 > table > tr:first-child > td > span').text()
        pages_ret = re.match(pattern_page, pages)
        if pages_ret:
            current_index = int(pages_ret.group(1))
            page_size = int(pages_ret.group(2))
            if 1 <= current_index <= page_size:
                next_form_data = common_formdata.copy()
                next_form_data['aim_page'] = str(current_index)
                next_form_data['page_count'] = str(page_size)
                self.crawl('http://www.pkulaw.cn/doSearch.ashx', method='POST', data=next_form_data,
                           callback=self.index_page, user_agent=UserAgent().random)
        # 逐条处理
        self.item_page(response)

    def item_page(self, response):
        ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if each.attr['class'] == 'main-ljwenzi' and re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, headers=common_detail_headers, callback=self.detail_page,
                           user_agent=ua.random)

    @config(priority=2)
    def detail_page(self, response):
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
                    elif u'截止日期' in strong:
                        td.children().remove()
                        ret['deadline'] = td.text().strip()

        ret['url'] = response.url
        ret['title'] = title.text().strip()
        main_content = response.doc('.Content > #div_content').html()
        ret['content'] = main_content.strip()

        # 保存mysql
        # 1. 时效性（是）：现行有效、尚未生效
        # 2. 效力级别（不是）：任免、工作文件、工作答复、部门工作文件、行政许可批复
        # 3. 具有截止日期字段：立法背景资料
        tmp_time_valid = ret.get('time_valid', '')
        tmp_deadline = ret.get('deadline', False)
        tmp_force_level = ret.get('force_level', '')
        if (u'现行有效' in tmp_time_valid or u'尚未生效' in tmp_time_valid or tmp_deadline) and (
                u'任免' not in tmp_force_level and
                u'工作文件' not in tmp_force_level and
                u'工作答复' not in tmp_force_level and
                u'部门工作文件' not in tmp_force_level and
                u'行政许可批复' not in tmp_force_level):
            self.save_to_mysql(ret)
        return ret

    # 保存到mysql
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO law(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline, appr_dept, appr_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('title', ''), ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('law_type', ''), ret.get('force_level', ''),
                ret.get('time_valid', ''), ret.get('impl_date', ''), ret.get('content', ''), ret.get('url', ''),
                ret.get('type', ''), ret.get('deadline', ''),
                ret.get('appr_dept', ''),
                ret.get('appr_date', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
