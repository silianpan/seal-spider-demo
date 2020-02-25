# -*- coding: utf-8 -*-

# Scrapy settings for pkulaw project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pkulaw'

SPIDER_MODULES = ['pkulaw.spiders']
NEWSPIDER_MODULE = 'pkulaw.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pkulaw (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'pkulaw.middlewares.PkulawSpiderMiddleware': 543
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
ZHIMA_PROXY_URL = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&pack=81983&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
ABUYUN_PROXY_SERVER = 'http://http-dyn.abuyun.com:9020'
ABUYUN_PROXY_USER = 'HV8L10RK3638731D'
ABUYUN_PROXY_PASS = '823956ADA0D112B7'
START_URL = 'http://www.pkulaw.cn/doSearch.ashx'
LOGIN_URL = 'http://www.pkulaw.cn/vip_login/CheckLogin.ashx?t=1&u=18582055881&p=asdf@123&n=1582595656673&menu_item=law'
LOGOUT_URL = 'http://www.pkulaw.cn/vip_login/CheckLogin.ashx?t=2&n=1582602847019&menu_item=law'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    # 'pkulaw.middlewares.ZhimaProxyMiddleware': 11,
    'pkulaw.middlewares.AbuyunProxyMiddleware': 11,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'pkulaw.middlewares.RandomUserAgentMiddleware': 10,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'pkulaw.middlewares.MyRetryMiddleware': 210,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'pkulaw.pipelines.PkulawPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.2
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [302, 403, 502, 500, 404]

# MySQL
MYSQL_HOST = '113.62.127.199'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'pkulaw_new'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Asdf@123'

# scrapy-redis
# 调度器和去重的类替换为scrapy-redis的类
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER = 'scrapy_redis_bloomfilter.scheduler.Scheduler'
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
DUPEFILTER_CLASS = 'scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter'
# 散列函数的个数，默认为6，可以自行修改
BLOOMFILTER_HASH_NUMBER = 6
# Bloom Filter的bit参数，默认30，占用128M空间，去重量级1亿
BLOOMFILTER_BIT = 30
# redis连接信息
REDIS_URL = 'redis://:asdf123@39.99.189.72:6379'
# 爬取全部完成后，不自动清空爬取队列和去重指纹集合
# 强制中断爬虫的运行，爬取队列和去重指纹集合是不会自动清空的
SCHEDULER_PERSIST = True
