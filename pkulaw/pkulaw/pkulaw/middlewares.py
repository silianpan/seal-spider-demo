# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import re

import requests
from pkulaw.ua.user_agent import UserAgent
from pkulaw.utils import is_expired
from scrapy import signals

logger = logging.getLogger(__name__)


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
    """
    代理中间件
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.start_url = settings.get('START_URL')
        self.proxy_url = settings.get('PROXY_URL')
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
            logger.debug('======使用代理：' + str(proxy) + '======')
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        url = request.url
        if (url == self.start_url or re.match(self.pattern_article, url)) and response.status != 200:
            if response.status in self.retry_http_codes:
                # 获取重试次数
                retries = request.meta.get('retry_times', 0)
                if retries >= self.max_retry_times:
                    # 更新代理列表，使用新代理
                    self.proxy_list = self.get_proxy_list()
                    new_proxy = self.get_random_proxy()
                    logger.debug('======已经达到最大重试次数，使用新代理：' + str(new_proxy) + '======')
                    request.meta['proxy'] = 'http://{proxy}'.format(proxy=new_proxy)
                    return request
            logger.warning('======返回异常，重试使用原代理：' + request.meta['proxy'] + '======')
            return request
        return response


class RandomUserAgentMiddleware(object):
    """
    UserAgent中间件
    """

    def __init__(self):
        self.user_agent = UserAgent()

    def process_request(self, request, spider):
        ua = self.user_agent.rget
        logger.debug('======使用User-Agent：' + str(ua) + '======')
        request.headers.setdefault('User-Agent', ua)

# class MyRetryMiddleware(RetryMiddleware):
#     """
#     重试中间件，更换代理
#     """
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def __init__(self, settings):
#         super().__init__(settings)
#         self.proxy_url = settings.get('PROXY_URL')
#
#     def get_proxy_list(self):
#         return requests.get(self.proxy_url).json()
#
#     def get_random_proxy(self):
#         proxy_list = self.get_proxy_list()
#         if proxy_list and proxy_list.get('code') == 0:
#             proxy_items = proxy_list.get('data')
#             for item in proxy_items:
#                 if not is_expired(item.get('expire_time')):
#                     return item.get('ip') + ':' + str(item.get('port'))
#         return self.get_random_proxy()
#
#     def process_response(self, request, response, spider):
#         if request.meta.get('dont_retry', False):
#             return response
#         if response.status in self.retry_http_codes:
#             # 获取重试次数
#             retries = request.meta.get('retry_times', 0)
#             if retries >= self.max_retry_times:
#                 new_proxy = self.get_random_proxy()
#                 logger.debug('======使用新代理：' + str(new_proxy) + '======')
#                 request.meta['proxy'] = 'http://{proxy}'.format(proxy=new_proxy)
#
#             # 获取返回原因
#             reason = response_status_message(response.status)
#             time.sleep(random.randint(3, 5))
#             logger.warning('======返回值异常, 更换代理，进行重试======')
#             return self._retry(request, reason, spider) or response
#         return response
#
#     def process_exception(self, request, exception, spider):
#         if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
#                 and not request.meta.get('dont_retry', False):
#             # 获取重试次数
#             retries = request.meta.get('retry_times', 0)
#             if retries >= self.max_retry_times:
#                 new_proxy = self.get_random_proxy()
#                 logger.debug('======使用新代理：' + str(new_proxy) + '======')
#                 request.meta['proxy'] = 'http://{proxy}'.format(proxy=new_proxy)
#
#             time.sleep(random.randint(3, 5))
#             logger.warning('======连接异常, 更换代理，进行重试======')
#
#             return self._retry(request, exception, spider)
