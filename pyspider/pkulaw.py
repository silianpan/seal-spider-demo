#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-14 15:19:11
# Project: pkulaw

import re

import pymysql
from pyspider.libs.base_handler import *

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
        pages = response.doc('ul.pagination-sm > li.disabled > label').text()
        if pages is not None and len(pages.strip()) != 0 and '/' in pages:
            pages_list = pages.split('/')
            if len(pages_list) == 2:
                tmp = pages_list[0]
                tmp_list = tmp.split(' ')
                # 当前页
                current_index = int(tmp_list[1]) + 1
                # 总页数
                page_size = int(pages_list[1])
                if 1 < current_index <= page_size:
                    # 回调index_page
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
                        'Pager.PageIndex': current_index - 1,
                        'RecordShowType': 'List',
                        'Pager.PageSize': 100,
                        'isEng': 'chinese',
                        'X-Requested-With': 'XMLHttpRequest',
                        'OldPageIndex': current_index - 2
                    }, callback=self.index_page)
        # 逐条处理
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
        li_list = response.doc('.content > .fields > ul > li').items()
        ret = {}
        for li in li_list:
            strong = li('strong').text()
            if strong is not None:
                if u'发布部门' in strong.strip():
                    cont = li('span').attr('title')
                    if cont is not None and len(cont.strip()) != 0:
                        ret['pub_dept'] = cont
                    else:
                        ret['pub_dept'] = li.attr('title')
                elif u'发文字号' in strong.strip():
                    ret['pub_no'] = li.attr('title')
                elif u'发布日期' in strong.strip():
                    # cont = li.attr('title')
                    # if cont is None or len(cont.strip()) == 0:
                    #     li.children().remove()
                    #     cont = li.text()
                    ret['pub_date'] = li.attr('title')
                elif u'实施日期' in strong.strip():
                    # cont = li.attr('title')
                    # if cont is None or len(cont.strip()) == 0:
                    #     li.children().remove()
                    #     cont = li.text()
                    ret['impl_date'] = li.attr('title')
                elif u'时效性' in strong.strip():
                    cont = li('span').attr('title')
                    if cont is not None and len(cont.strip()) != 0:
                        ret['time_valid'] = cont
                    else:
                        ret['time_valid'] = li.attr('title')
                elif u'效力级别' in strong.strip():
                    ret['force_level'] = li('span').attr('title')
                    # if cont is not None and len(cont.strip()) != 0:
                    #     ret['force_level'] = cont
                    # else:
                    #     ret['force_level'] = li.attr('title')
                elif u'法规类别' in strong.strip():
                    ret['law_type'] = li('span').attr('title')
                    # if cont is not None and len(cont.strip()) != 0:
                    #     ret['law_type'] = cont
                    # else:
                    #     ret['law_type'] = li.attr('title')
                elif u'类别' in strong.strip():
                    ret['type'] = li('a').text()
                elif u'截止日期' in strong.strip():
                    li.children().remove()
                    cont = li.text()
                    # if cont is None or len(cont.strip()) == 0:
                    #     cont = li.attr('title')
                    ret['deadline'] = cont

        ret['url'] = response.url
        ret['title'] = title.text().strip()
        ret['content'] = response.doc('.content > .fulltext').html().strip()

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
        # try:
        #     cursor.execute(sql, params)
        #     db.commit()
        # except:
        #     db.rollback()
        cursor.execute(sql, params)
        db.commit()
        cursor.close()
        db.close()
