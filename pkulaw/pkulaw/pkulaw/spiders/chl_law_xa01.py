#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-04 23:41
# @Author  : liupan
# @Site    : 
# @File    : chl_law_xa01.py
# @Software: PyCharm

"""
    scrapy初始Url的两种写法，
    一种是常量start_urls，并且需要定义一个方法parse（）
    另一种是直接定义一个方法：star_requests()
"""
import re

import scrapy

pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')

start_url = 'http://www.pkulaw.cn/doSearch.ashx'

clusterwhere = '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXA01'
db = 'chl'
menu_item = 'law'
referer = 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&'

formdata = {
    'Db': db,
    'clusterwhere': clusterwhere,
    'clust_db': db,
    'range': 'name',
    'menu_item': menu_item
}
headers = {
    'Origin': 'http://www.pkulaw.cn',
    'Referer': referer,
    'Host': 'www.pkulaw.cn',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}
cookies = {
    'isCheck': 'ValidateSuccess_126',
    'codeCompare': 'OK_126'
}


class ChlLawXa01(scrapy.Spider):
    name = 'chlLawXa01'

    # start_urls = [  # 另外一种写法，无需定义start_requests方法
    #     'http://lab.scrapyd.cn/page/1/',
    #     'http://lab.scrapyd.cn/page/2/',
    # ]

    # 另外一种初始链接写法
    def start_requests(self):
        yield scrapy.FormRequest(url=start_url, method='POST', headers=headers, cookies=cookies, formdata=formdata,
                                 callback=self.parse, dont_filter=True)

    # 如果是简写初始url，此方法名必须为：parse
    def parse(self, response):
        href_list = response.css('a.main-ljwenzi::attr(href)').extract_first()
        for href in href_list:
            href = response.urljoin(href)
            if re.match(pattern_article, href):
                yield scrapy.Request(url=href, headers=headers, cookies=cookies, callback=self.parse_detail,
                                     dont_filter=True)

        pages = response.css('.main-top4-1 > table > tr:first-child > td > span::text').extract_first()
        pages_ret = re.match(pattern_page, pages)
        if pages_ret:
            current_index = int(pages_ret.group(1))
            page_size = int(pages_ret.group(2))
            if 1 <= current_index <= page_size:
                next_formdata = {
                    'range': 'name',
                    'Db': db,
                    'clusterwhere': clusterwhere,
                    'aim_page': str(current_index),
                    'page_count': str(page_size),
                    'clust_db': db,
                    'menu_item': menu_item
                }
                yield scrapy.FormRequest(url=start_url, method='POST', headers=headers, cookies=cookies,
                                         formdata=next_formdata,
                                         callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        title = response.css('table#tbl_content_main > tr:first-child > td > span > strong::text').extract_first()
        li_list = response.css('table#tbl_content_main > tr')
        ret = {}
        for li in li_list:
            td_list = li.css('td')
            for td in td_list:
                strong = td.css('font::text').extract_first()
                if strong is not None:
                    strong = strong.strip()
                    if u'发布部门' in strong:
                        ret['pub_dept'] = td.css('a::text').extract_first().strip()
                    elif u'发文字号' in strong:
                        ret['pub_no'] = td.xpath('./text()').extract_first().strip()
                    elif u'发布日期' in strong:
                        ret['pub_date'] = td.xpath('./text()').extract_first().strip()
                    elif u'实施日期' in strong:
                        ret['impl_date'] = td.xpath('./text()').extract_first().strip()
                    elif u'时效性' in strong:
                        ret['time_valid'] = td.css('a::text').extract_first().strip()
                    elif u'效力级别' in strong:
                        ret['force_level'] = td.css('a::text').extract_first().strip()
                    elif u'法规类别' in strong:
                        ret['law_type'] = td.css('a::text').extract_first().strip()
                    elif u'类别' in strong:
                        ret['type'] = td.css('a::text').extract_first().strip()
                    elif u'截止日期' in strong.strip():
                        ret['deadline'] = td.text().strip()

        ret['url'] = response.url
        ret['title'] = title.strip()
        main_content = response.css('.Content > #div_content').extract_first()
        ret['content'] = main_content.strip()

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
            yield ret
