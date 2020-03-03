#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    :
# @File    : pkulaw_open.py
# @Software: PyCharm

import json

from fake_useragent import UserAgent
from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysql_util import MysqlUtil

start_url = 'http://open.pkulaw.cn/Search/Record'

common_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'open.pkulaw.cn',
    'Origin': 'http://open.pkulaw.cn',
    'Referer': 'http://open.pkulaw.cn/',
    'User-Agent': UserAgent().random,
    'X-Requested-With': 'XMLHttpRequest'
}

all_form_data = [
    {
        'Menu': 'LAW',
        'IsFullTextSearch': 'False',
        'MatchType': 'Exact',
        'OrderByIndex': '0',
        'GroupByIndex': '0',
        'ShowType': '1',
        'Library': 'CHL',
        'GroupIndex': '0',
        'GroupValue': 'xa0101',
        'X-Requested-With': 'XMLHttpRequest',
        'SubKeyword': '在结果的标题中检索'
    },
    {
        'Menu': 'LAW',
        'IsFullTextSearch': 'False',
        'MatchType': 'Exact',
        'OrderByIndex': '0',
        'GroupByIndex': '0',
        'ShowType': '1',
        'Library': 'CHL',
        'GroupIndex': '0',
        'GroupValue': 'xc0201',
        'X-Requested-With': 'XMLHttpRequest',
        'SubKeyword': '在结果的标题中检索'
    },
    {
        'Menu': 'LAW',
        'IsFullTextSearch': 'False',
        'MatchType': 'Exact',
        'OrderByIndex': '0',
        'GroupByIndex': '0',
        'ShowType': '1',
        'Library': 'CHL',
        'GroupIndex': '0',
        'GroupValue': 'xg0401',
        'X-Requested-With': 'XMLHttpRequest',
        'SubKeyword': '在结果的标题中检索'
    }
]

class Handler(BaseHandler):
    crawl_config = {
    }

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        for form_data in all_form_data:
            self.crawl(start_url, method='POST', headers=common_headers, data=form_data, user_agent=UserAgent().random, callback=self.index_page, save={'form_data': form_data})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        item_list = response.doc('.contentList > dd > a').items()
        for item in item_list:
            detail_href = item.attr('href')
            self.crawl(detail_href, user_agent=UserAgent().random, callback=self.detail_page)

        form_data = response.save.get('form_data', False)
        if form_data:
            pagenumber = int(response.doc('#spanPagerMessage .qp_pagenumber').text())
            totalnumber = int(response.doc('#spanPagerMessage .qp_totalnumber').text())
            if pagenumber < totalnumber:
                next_form_data = form_data.copy()
                next_form_data['Pager.PageSize'] = 100
                next_form_data['Pager.PageIndex'] = pagenumber
                self.crawl(start_url, method='POST', headers=common_headers, data=next_form_data, user_agent=UserAgent().random, callback=self.index_page,
                           save={'form_data': next_form_data})


    @config(priority=2)
    def detail_page(self, response):
        if response.status_code == 500:
            return
        title = response.doc('.article > h3').text()
        if not title:
            title = response.doc('title').text()
        ret = {
            "url": response.url,
            "title": title,
            "content": response.doc('.articleText').html().strip(),
            "remark": 'http://open.pkulaw.cn'
        }
        li_list = response.doc('.articleInfo > li').items()
        for li in li_list:
            strong = li('strong').text()
            if u'法规类别' in strong:
                ret['law_type'] = li('a').text()
            elif u'发文字号' in strong:
                ret['pub_no'] = li('a').text()
            elif u'发布部门' in strong:
                ret['pub_dept'] = li('a').text()
            elif u'发布日期' in strong:
                li.children().remove()
                ret['pub_date'] = li.text()
            elif u'实施日期' in strong:
                li.children().remove()
                ret['impl_date'] = li.text()
            elif u'时效性' in strong:
                ret['time_valid'] = li('a').text()
            elif u'效力级别' in strong:
                ret['force_level'] = li('a').text()

        return ret

    def on_result(self, result):
        if result and result['title'] and result['content']:
            sql = MysqlUtil()
            sql.insert('law', **result)
