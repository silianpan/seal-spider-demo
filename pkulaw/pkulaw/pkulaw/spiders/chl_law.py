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
from pkulaw.items import PkulawItem

pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')

start_url = 'http://www.pkulaw.cn/doSearch.ashx'

Db = 'chl'
clust_db = 'chl'
menu_item = 'law'
referer = 'http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&keyword=&range=name&'

Db_city = 'lar'
clust_db_city = 'lar'
referer_city = 'http://www.pkulaw.cn/cluster_form.aspx?Db=lar&menu_item=law&EncodingName=&keyword=&range=name&'

Db_proto = 'protocol,lawexplanation,whitebook,workreport,introduction'
clust_db_proto = 'protocol'
menu_item_proto = 'lfbj_all'
Search_Mode = 'accurate'
referer_proto = 'http://www.pkulaw.cn/cluster_call_form.aspx?Db=protocol&menu_item=lfbj_all&EncodingName=&keyword=&range=name&'

common_headers = {
    'Origin': 'http://www.pkulaw.cn',
    'Host': 'www.pkulaw.cn',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}
common_cookies = {
    'isCheck': 'ValidateSuccess_126',
    'codeCompare': 'OK_126'
}

all_options = [
    # xa01 中央法规-法律
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXA01'
        }
    },
    # xc02 中央法规-行政法规
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXC02'
        }
    },
    # xe03 中央法规-部门规章
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXE03'
        }
    },
    # xg04 中央法规-司法解释
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXG04'
        }
    },
    # xi05 中央法规-团体规定
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXI05'
        }
    },
    # xk06 中央法规-行业规定
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXK06'
        }
    },
    # xr12 中央法规-党内法规
    {
        'Referer': referer,
        'formdata': {
            'Db': Db,
            'clust_db': clust_db,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e6%2595%2588%25e5%258a%259b%25e7%25ba%25a7%25e5%2588%25ab%253dXR12'
        }
    },
    # 地方法规-甘肃
    {
        'Referer': referer_city,
        'formdata': {
            'Db': Db_city,
            'clust_db': clust_db_city,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e5%258f%2591%25e5%25b8%2583%25e9%2583%25a8%25e9%2597%25a8%253d826'
        }
    },
    # 地方法规-青海
    {
        'Referer': referer_city,
        'formdata': {
            'Db': Db_city,
            'clust_db': clust_db_city,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e5%258f%2591%25e5%25b8%2583%25e9%2583%25a8%25e9%2597%25a8%253d827'
        }
    },
    # 地方法规-四川
    {
        'Referer': referer_city,
        'formdata': {
            'Db': Db_city,
            'clust_db': clust_db_city,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e5%258f%2591%25e5%25b8%2583%25e9%2583%25a8%25e9%2597%25a8%253d821'
        }
    },
    # 地方法规-西藏
    {
        'Referer': referer_city,
        'formdata': {
            'Db': Db_city,
            'clust_db': clust_db_city,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e5%258f%2591%25e5%25b8%2583%25e9%2583%25a8%25e9%2597%25a8%253d824'
        }
    },
    # 地方法规-云南
    {
        'Referer': referer_city,
        'formdata': {
            'Db': Db_city,
            'clust_db': clust_db_city,
            'menu_item': menu_item,
            'range': 'name',
            'clusterwhere': '%25e5%258f%2591%25e5%25b8%2583%25e9%2583%25a8%25e9%2597%25a8%253d823'
        }
    },
    # 立法资料-中央
    {
        'Referer': referer_proto,
        'formdata': {
            'Db': Db_proto,
            'clust_db': clust_db_proto,
            'menu_item': menu_item_proto,
            'range': 'name',
            'clusterwhere': '%25e6%2589%2580%25e5%25b1%259e%25e8%258c%2583%25e5%259b%25b4%253d0',
            'Search_Mode': Search_Mode
        }
    },
    # 立法资料-地方
    {
        'Referer': referer_proto,
        'formdata': {
            'Db': Db_proto,
            'clust_db': clust_db_proto,
            'menu_item': menu_item_proto,
            'range': 'name',
            'clusterwhere': '%25e6%2589%2580%25e5%25b1%259e%25e8%258c%2583%25e5%259b%25b4%253d1',
            'Search_Mode': Search_Mode
        }
    }
]


class ChlLaw(scrapy.Spider):
    name = 'chlLaw'

    # 另外一种初始链接写法
    def start_requests(self):
        for option_item in all_options:
            headers = common_headers.copy()
            headers['Referer'] = option_item['Referer']
            formdata = option_item['formdata']
            callback_options = {
                'headers': headers,
                'formdata': formdata,
                'cookies': common_cookies
            }
            yield scrapy.FormRequest(url=start_url, method='POST', headers=headers, cookies=common_cookies, formdata=formdata,
                                     callback=self.parse, meta={'callback_options': callback_options}, dont_filter=True)

    # 如果是简写初始url，此方法名必须为：parse
    def parse(self, response):
        headers = response.meta['callback_options']['headers']
        formdata = response.meta['callback_options']['formdata']
        cookies = response.meta['callback_options']['cookies']

        href_list = response.css('a.main-ljwenzi::attr(href)').extract()
        for href in href_list:
            href = response.urljoin(href)
            if re.match(pattern_article, href):
                yield scrapy.Request(url=href, headers=headers, cookies=cookies, callback=self.parse_detail,
                                     dont_filter=False)

        pages = response.css('.main-top4-1 > table > tr:first-child > td > span::text').extract_first()
        pages_ret = re.match(pattern_page, pages)
        if pages_ret:
            current_index = int(pages_ret.group(1))
            page_size = int(pages_ret.group(2))
            if 1 <= current_index <= page_size:
                next_formdata = formdata.copy()
                next_formdata['aim_page'] = str(current_index)
                next_formdata['page_count'] = str(page_size)
                yield scrapy.FormRequest(url=start_url, method='POST', headers=headers, cookies=cookies,
                                         formdata=next_formdata,
                                         callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        title = response.css('table#tbl_content_main > tr:first-child > td > span > strong::text').extract_first()
        li_list = response.css('table#tbl_content_main > tr')
        ret = PkulawItem()
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
                                                                               ret['force_level'] and u'部门工作文件' not in
                                                                               ret['force_level'] and
                                                                               u'行政许可批复' not in ret[
                                                                                   'force_level']):
            if 'appr_dept' not in ret:
                ret['appr_dept'] = ''
            if 'appr_date' not in ret:
                ret['appr_date'] = ''
            if 'deadline' not in ret:
                ret['deadline'] = ''
            if 'type' not in ret:
                ret['type'] = ''
            if 'pub_no' not in ret:
                ret['pub_no'] = ''
            yield ret
