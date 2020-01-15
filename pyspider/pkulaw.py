#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-14 15:19:11
# Project: pkulaw

from pyspider.libs.base_handler import *
import re

# 正则表达式
pattern_article = re.compile('^https://www.pkulaw.com/chl/\w{20}.html$')

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Referer': 'https://www.pkulaw.com/',
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
        self.crawl('https://www.pkulaw.com/law/search/RecordSearch', method='POST', data={
            'Menu': 'law',
            'SearchKeywordType': 'DefaultSearch',
            'MatchType': 'Exact',
            'RangeType': 'Piece',
            'Library': 'chl',
            'ClassFlag': 'chl',
            'QueryOnClick': 'False',
            'AfterSearch': 'False',
            'IsSynonymSearch': 'true',
            'IsAdv': 'False',
            'ClassCodeKey': ',XA01,,,,',
            'GroupByIndex': 0,
            'OrderByIndex': 0,
            'ShowType': 'Default',
            'Pager.PageIndex': 0,
            'RecordShowType': 'List',
            'Pager.PageSize': 100,
            'isEng': 'chinese',
            'X-Requested-With': 'XMLHttpRequest'
        }, callback=self.index_page)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        # 后续分页处理
        pages = response.doc('ul.pagination-sm > li.disabled > label').text()
        if pages is not None and len(pages.strip()) != 0 and '/' in pages:
            pages_list = pages.split('/')
            if len(pages_list) == 2:
                page_size = pages_list[1]
                for page_index in range(1, int(page_size)):
                    self.crawl('https://www.pkulaw.com/law/search/RecordSearch', method='POST', data={
                        'Menu': 'law',
                        'SearchKeywordType': 'DefaultSearch',
                        'MatchType': 'Exact',
                        'RangeType': 'Piece',
                        'Library': 'chl',
                        'ClassFlag': 'chl',
                        'QueryOnClick': 'False',
                        'AfterSearch': 'False',
                        'IsSynonymSearch': 'true',
                        'IsAdv': 'False',
                        'ClassCodeKey': ',XA01,,,,',
                        'GroupByIndex': 0,
                        'OrderByIndex': 0,
                        'ShowType': 'Default',
                        'Pager.PageIndex': page_index,
                        'RecordShowType': 'List',
                        'Pager.PageSize': 100,
                        'isEng': 'chinese',
                        'X-Requested-With': 'XMLHttpRequest',
                        'OldPageIndex': page_index - 1
                    }, callback=self.item_page)
        # 第一页处理
        self.item_page(response)

    @config(priority=2)
    def item_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=3)
    def detail_page(self, response):
        # 详细处理
        title = response.doc('.content > .title')
        title.children().remove()
        fields = response.doc('.content > .fields > ul')
        return {
            "url": response.url,
            "title": title.text(),
            "pub_dept": fields('li:first-child > span').attr('title'),
            "pub_no": fields('li:nth-child(2)').attr('title'),
            "pub_date": fields('li:nth-child(3)').attr('title'),
            "impl_date": fields('li:nth-child(4)').attr('title'),
            "now_valid": fields('li:nth-child(5) > span').attr('title'),
            "level": fields('li:nth-child(6) > span').attr('title'),
            "type": fields('li:last-child > span').attr('title')
        }
