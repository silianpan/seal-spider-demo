# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import logging
import re

import requests
from pkulaw.ua.user_agent import UserAgent
from pkulaw.utils import is_expired

logger = logging.getLogger(__name__)


class AbuyunProxyMiddleware(object):
    """
    阿布云代理中间件
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.abuyun_proxy_server = settings.get('ABUYUN_PROXY_SERVER')
        abuyun_proxy_user = settings.get('ABUYUN_PROXY_USER')
        abuyun_proxy_pass = settings.get('ABUYUN_PROXY_PASS')
        self.abuyun_proxy_auth = "Basic " + base64.urlsafe_b64encode(
            bytes((abuyun_proxy_user + ":" + abuyun_proxy_pass), "ascii")).decode("utf8")

    def process_request(self, request, spider):
        request.meta["proxy"] = self.abuyun_proxy_server
        request.headers["Proxy-Authorization"] = self.abuyun_proxy_auth


class ZhimaProxyMiddleware(object):
    """
    芝麻代理中间件
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.start_url = settings.get('START_URL')
        self.proxy_url = settings.get('ZHIMA_PROXY_URL')
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
        # 自己的url，返回错误
        if (url == self.start_url or re.match(self.pattern_article, url)) and response.status != 200:
            logger.error('############status: ' + str(response.status) + '###############')
            logger.error('############flags: ' + str(response.flags) + '###############')
            logger.error('############body: ' + str(
                response.body.decode('utf8') if response.body else response.body) + '###############')
            # 1. IP被封了，更新代理
            if response.status == 403:
                self.update_proxy(request)
                return request
            # 2. 获取重试次数，大于最大重试次数，更新代理
            # if response.status in self.retry_http_codes:
            retries = request.meta.get('retry_times', 0)
            if retries >= self.max_retry_times:
                self.update_proxy(request)
                return request
            logger.warning('======返回异常' + str(response.status) + '，重试使用原代理：' + request.meta['proxy'] + '======')
            return request
        return response

    def update_proxy(self, request):
        """
        重新通过api获取代理，更新代理
        :param request:
        :return:
        """
        # 重新通过api获取代理
        self.proxy_list = self.get_proxy_list()
        new_proxy = self.get_random_proxy()
        logger.debug('======已经达到最大重试次数或者IP被封，使用新代理：' + str(new_proxy) + '======')
        request.meta['proxy'] = 'http://{proxy}'.format(proxy=new_proxy)


class RandomUserAgentMiddleware(object):
    """
    UserAgent中间件
    """

    def __init__(self):
        self.user_agent = UserAgent('chrome')

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
#         self.proxy_url = settings.get('ZHIMA_PROXY_URL')
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
