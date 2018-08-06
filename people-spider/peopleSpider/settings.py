# -*- coding: utf-8 -*-
import os
# Scrapy settings for peopleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'peopleSpider'

SPIDER_MODULES = ['peopleSpider.spiders']
NEWSPIDER_MODULE = 'peopleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400']

# PROXIES = [
#
# ]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': '*/*',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
# }
# HTTPERROR_ALLOWED_CODES = [403]
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'peopleSpider.middlewares.PeoplespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 在此设置请求头和代理，对应类路径
   'peopleSpider.middlewares.PeopleUserAgentMiddleware': 1,
   # 'peopleSpider.middlewares.RandomUserAgentMiddlware': 1,
   'peopleSpider.middlewares.ProxyMiddleware': 2,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 下载图片
   'peopleSpider.pipelines.TetePipeline': 100,
   # 输出json
   'peopleSpider.pipelines.JsonExporterPipleline': 180,
   # 输出excel
   # 'peopleSpider.pipelines.TuniuPipeline': 200,
}

RANDOM_UA_TYPE = "random"
#  文件下载路径
FILES_STORE = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = os.path.dirname(os.path.abspath(__file__)) + 'downImages'
FEED_EXPORT_ENCODING = 'utf-8'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 8
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = ""
MYSQL_DBNAME = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""