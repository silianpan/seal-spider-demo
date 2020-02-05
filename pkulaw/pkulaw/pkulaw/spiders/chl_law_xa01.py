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

clusterwhere = '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXA01'
db = 'chl'
menu_item = 'law'
referer = 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&'

pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')


class ChlLawXa01(scrapy.Spider):
    name = 'chlLawXa01'

    # start_urls = [  # 另外一种写法，无需定义start_requests方法
    #     'http://lab.scrapyd.cn/page/1/',
    #     'http://lab.scrapyd.cn/page/2/',
    # ]

    # 另外一种初始链接写法
    def start_requests(self):
        url = 'http://www.pkulaw.cn/doSearch.ashx'
        data = {
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
        yield scrapy.FormRequest(url=url, method='POST', headers=headers, cookies=cookies, formdata=data,
                                 callback=self.parse, dont_filter=True)

    # 如果是简写初始url，此方法名必须为：parse
    def parse(self, response):
        href = response.xpath('//a[@class="main-ljwenzi"]//@href').extract_first()
        href = response.urljoin(href)
        if re.match(pattern_article, href):
            title = response.xpath('//a[@class="main-ljwenzi"]/text()').extract()
            print(title)
