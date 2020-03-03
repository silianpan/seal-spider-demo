#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 下午3:25
# @Author  : liupan
# @Site    : 
# @File    : china_court.py
# @Software: PyCharm

from fake_useragent import UserAgent
from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysql_util import MysqlUtil

start_url = 'https://www.chinacourt.org/law.shtml'


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, user_agent=UserAgent().random, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        menu_title_list = response.doc('ul.biaoti > li > a').items()
        for menu_title in menu_title_list:
            menu_text = menu_title.text()
            menu_href = menu_title.attr('href')
            if u'中外条约' != menu_text and u'立法追踪' != menu_text:
                self.crawl(menu_href, user_agent=UserAgent().random, callback=self.item_page)

    def item_page(self, response):
        news_list = response.doc('.law_list > ul > li').items()
        for news in news_list:
            news_href = news('.left > a').attr('href')
            pub_date = news('.right').text()
            self.crawl(news_href, user_agent=UserAgent().random, callback=self.detail_page, save={'pub_date': pub_date})
        # 下一页
        next_list = response.doc('.paginationControl > a').items()
        for next_page in next_list:
            if u'下一页' == next_page.text():
                next_href = next_page.attr('href')
                self.crawl(next_href, user_agent=UserAgent().random, callback=self.item_page)
                break

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.content_text > div,p[style="text-align:center;"]:lt(4) > strong').text()
        if not title:
            title = response.doc('.content_text > div,p[style="text-align: center;"]:lt(4) > strong').text()
        if not title:
            title = response.doc('.content_text > p[style="text-align:center;"]:lt(4) > strong').text()
        if not title:
            title = response.doc('.content_text > p[style="text-align: center;"]:lt(4) > strong').text()
        if not title:
            title = response.doc('.content_text > p:lt(3) > span > strong').text()
        if not title:
            title = response.doc('.content_text > p:lt(3) > strong').text()
        if not title:
            title = response.doc('.MTitle').text()
        if not title:
            title = response.doc('.content_text > div,p[style="text-align:center;"]:lt(4)').text()
        if not title:
            title = response.doc('.content_text > p[align="center"] > strong').text()
        if not title:
            title = response.doc('.MsoPlainText > strong > span').text()
        if len(title) > 255:
            title = title[:255]
        content = response.doc('.content_text').html().strip()
        ret = {
            "url": response.url,
            "title": title,
            "pub_date": response.save.get('pub_date', ''),
            "content": content,
            "remark": 'https://www.chinacourt.org/law.shtml'
        }
        stitle = response.doc('.STitle').html().strip()
        for sitem in stitle.split(r'<br />'):
            if sitem:
                ret_item_list = sitem.strip().split(u'】')
                if len(ret_item_list) == 2:
                    if u'发布单位' in ret_item_list[0]:
                        ret['pub_dept'] = ret_item_list[1].strip()
                    elif u'发布文号' in ret_item_list[0]:
                        ret['pub_no'] = ret_item_list[1].strip()
                    elif u'发布日期' in ret_item_list[0]:
                        ret['pub_date'] = ret_item_list[1].strip()
                    elif u'生效日期' in ret_item_list[0]:
                        ret['impl_date'] = ret_item_list[1].strip()
                    elif u'失效日期' in ret_item_list[0]:
                        ret['deadline'] = ret_item_list[1].strip()
                    elif u'所属类别' in ret_item_list[0]:
                        ret['law_type'] = ret_item_list[1].strip()
                    elif u'所属类别' in ret_item_list[0]:
                        ret['law_type'] = ret_item_list[1].strip()
        return ret

    def on_result(self, result):
        if result and result['title'] and result['content']:
            sql = MysqlUtil()
            sql.insert('law', **result)
