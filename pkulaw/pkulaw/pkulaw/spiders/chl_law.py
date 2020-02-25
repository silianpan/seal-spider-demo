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
import logging
import re

import scrapy
from pkulaw.items import PkulawItem
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)

pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')
pattern_page = re.compile(u'^.*第\s+(\d+)\s+.*共\s+(\d+)\s+.*$')

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

login_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.pkulaw.cn',
    'Referer': 'http://www.pkulaw.cn/vip_login/vip_login.aspx?menu_item=law&EncodingName=',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:73.0) Gecko/20100101 Firefox/73.0'
}

common_headers = {
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
common_cookies = {
    'isCheck': 'ValidateSuccess_126',
    'codeCompare': 'OK_126',
    'QINGCLOUDELB': '31b817f86975363201940f8e0a50b7bee13319b57ab5f3b439cc153975d86b02',
    'User_User': 'phone2020022509122640225'
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

    def __init__(self, settings, *args, **kwargs):
        super(ChlLaw, self).__init__(*args, **kwargs)
        self.start_url = settings.get('START_URL')
        self.login_url = settings.get('LOGIN_URL')
        self.logout_url = settings.get('LOGOUT_URL')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    # 另外一种初始链接写法
    def start_requests(self):
        # 登陆请求
        # yield scrapy.Request(url=self.logout_url, headers=login_headers, callback=self.login_after)
        # yield scrapy.Request(url=self.login_url, headers=login_headers, callback=self.login_after)

        for option_item in all_options:
            headers = common_headers.copy()
            headers['Referer'] = option_item['Referer']
            formdata = option_item['formdata']
            callback_options = {
                'headers': headers,
                'formdata': formdata,
                'cookies': common_cookies
            }
            yield scrapy.FormRequest(url=self.start_url, method='POST', headers=headers, cookies=common_cookies,
                                     formdata=formdata,
                                     callback=self.parse,
                                     meta={'callback_options': callback_options, 'dont_redirect': True,
                                           'handle_httpstatus_list': [302]}, dont_filter=True)

    # def login_after(self, response):
    #     print(response.body.decode('gbk'))

    # 如果是简写初始url，此方法名必须为：parse
    def parse(self, response):
        callback_options = response.meta.get('callback_options')
        headers = callback_options.get('headers')
        formdata = callback_options.get('formdata')
        cookies = callback_options.get('cookies')

        tmp_detail_headers = common_detail_headers.copy()
        tmp_detail_headers['Referer'] = headers['Referer']
        # href_list = response.css('a.main-ljwenzi::attr(href)').extract()

        sub_title_items = response.xpath('//span[@style="color:#727272;font-size:13px;"]')
        for sub_title in sub_title_items:
            sub_title_text = sub_title.xpath('string(.)').get()
            if u'失效' not in sub_title_text and u'已被修改' not in sub_title_text and u'部分失效' not in sub_title_text:
                href = sub_title.xpath('./../../preceding-sibling::tr[1]//a[@class="main-ljwenzi"]/@href').get()
                title = sub_title.xpath('./../../preceding-sibling::tr[1]//a[@class="main-ljwenzi"]/text()').get()
                # 需要进一步获取明细的条件
                # 如果有标题，且不在xxx
                if title and u'任免' not in title and title[-2:] not in [u'意见', u'答复', u'公告', u'报告', u'批复', u'通知', u'通告']:
                    href = response.urljoin(href)
                    # if re.match(pattern_article, href):
                    yield scrapy.Request(url=href, headers=tmp_detail_headers, cookies=cookies,
                                         callback=self.parse_detail,
                                         meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
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
                yield scrapy.FormRequest(url=self.start_url, method='POST', headers=headers, cookies=cookies,
                                         formdata=next_formdata,
                                         callback=self.parse,
                                         meta={'callback_options': callback_options, 'dont_redirect': True,
                                               'handle_httpstatus_list': [302]},
                                         dont_filter=True)

    def parse_detail(self, response):
        title = response.css('table#tbl_content_main > tr:first-child > td > span > strong::text').extract_first()
        logger.info(title)
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
                    elif u'截止日期' in strong:
                        ret['deadline'] = td.xpath('./text()').extract_first().strip()

        ret['url'] = response.url
        ret['title'] = title.strip() if title else response.css('title::text').get()
        main_content = response.css('.Content > #div_content').extract_first()
        if main_content is None:
            logger.error('############body: ' + str(response.body.decode('utf8') if response.body else response.body) + '###############')
            raise DropItem('main_content is None!')
        ret['content'] = main_content.strip()
        yield ret

        # 保存mysql
        # 1. 时效性（是）：现行有效、尚未生效
        # 2. 效力级别（不是）：任免、工作文件、工作答复、部门工作文件、行政许可批复
        # 3. 具有截止日期字段：立法背景资料
        # tmp_time_valid = ret.get('time_valid', '')
        # tmp_deadline = ret.get('deadline', False)
        # tmp_force_level = ret.get('force_level', '')
        # if (u'现行有效' in tmp_time_valid or u'尚未生效' in tmp_time_valid or tmp_deadline) and (
        #         u'任免' not in tmp_force_level and
        #         u'工作文件' not in tmp_force_level and
        #         u'工作答复' not in tmp_force_level and
        #         u'部门工作文件' not in tmp_force_level and
        #         u'行政许可批复' not in tmp_force_level):
        #     yield ret
