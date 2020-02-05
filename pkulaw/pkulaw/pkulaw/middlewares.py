# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import re
import logging

import requests
from fake_useragent import UserAgent
from pkulaw.utils import is_expired
from scrapy import signals


class PkulawSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PkulawDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL'),
            start_url=settings.get('START_URL')
        )

    def __init__(self, proxy_url, start_url):
        self.logger = logging.getLogger(__name__)
        self.start_url = start_url
        self.proxy_url = proxy_url
        self.proxy_list = self.get_proxy_list()
        self.pattern_article = re.compile(u'^http://www.pkulaw.cn/fulltext_form.aspx\?.+$')

    def get_proxy_list(self):
        return requests.get(self.proxy_url).json()

    def get_random_proxy(self):
        if self.proxy_list and self.proxy_list.get('code') == 0:
            proxy_items = self.proxy_list.get('data')
            for item in proxy_items:
                if not is_expired(item.get('expire_time')):
                    return item.get('ip') + ':' + str(item.get('port'))
        self.proxy_list = self.get_proxy_list()
        return self.get_random_proxy()

    def process_request(self, request, spider):
        url = request.url
        if url == self.start_url or re.match(self.pattern_article, url):
            proxy = self.get_random_proxy()
            self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        url = request.url
        if (url == self.start_url or re.match(self.pattern_article, url)) and response.status != 200:
            self.logger.debug('======返回获取代理======')
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=self.get_random_proxy())
            return request
        return response


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_agent = UserAgent()

    def process_request(self, request, spider):
        ua = self.user_agent.random
        self.logger.debug('======' + '使用User-Agent ' + str(ua) + "======")
        request.headers.setdefault('User-Agent', ua)

    def process_response(self, request, response, spider):
        if response.status != 200:
            self.logger.debug('======重新获取User-Agent======')
            request.headers.setdefault('User-Agent', self.user_agent.random)
            return request
        return response