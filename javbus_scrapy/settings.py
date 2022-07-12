# Scrapy settings for javbus_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from datetime import datetime

BOT_NAME = 'javbus_scrapy'

SPIDER_MODULES = ['javbus_scrapy.spiders']
NEWSPIDER_MODULE = 'javbus_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'javbus_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

DOWNLOADER_CLIENT_TLS_METHOD = "TLSv1.2"

# Disable cookies (enabled by default)
# 如果设置为True  那么久不可以在header中设置cookie
# 就需要在scrapy.Request 中传入命名参数 cookies = {}
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 这里不使用默认的请求头
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'javbus_scrapy.middlewares.JavbusScrapySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'javbus_scrapy.middlewares.JavbusScrapyDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'javbus_scrapy.pipelines.JavbusScrapyPipeline': 300,
    'javbus_scrapy.pipelines.JavbusScrapyActressesPipeline': 400,
    'javbus_scrapy.pipelines.JavbusScrapyStarItemInfoPipeline': 500,
    'javbus_scrapy.pipelines.JavbusScrapyStarInfoPipeline': 600,
    'javbus_scrapy.pipelines.JavbusScrapyMovieDetailsPipeline': 700,
    'javbus_scrapy.pipelines.JavbusScrapyMovieTorrentsPipeline': 800,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 数据库共用
# MYSQL_HOST = '192.168.11.117'
# MYSQL_DBNAME = {"scrapy_pie": "scrapy_pie_db"}
# MYSQL_USER = 'root'
# MYSQL_PASS = 'sunriseme1994'

# # 配置数据的保存目录
DATA_STORE = './data_store'
# 只爬取censored censored uncensored all
CENSORED = 'uncensored'

DOMAIN_BASE_URL = "https://www.javbus.com"
ACTRESSES_PATH_NAME = "actresses"
STARINFO_PATH_NAME = "starinfo"
STARITEMINFO_PATH_NAME = "stariteminfo"
MOVIE_DETAIL_PATH_NAME = "moviedetail"
TORRENT_DETAIL_PATH_NAME = "torrentdetail"
REQUESTS_PROXIES = {
    'http': 'http://127.0.0.1:7892',
    'https': 'http://127.0.0.1:7892',
}

# 文件及路径，log目录需要先建好
today = datetime.now()
setting_dir = os.path.dirname(__file__)
log_dir = os.path.dirname(setting_dir)
log_dir = os.path.join(log_dir, "logs")

# 日志输出
# LOG_LEVEL = 'ERROR'
LOG_LEVEL = 'DEBUG'

# 开启log file 日志输出就不回输出到控制台了
LOG_FILE = log_dir + "/" + "scrapy_{}_{}_{}:{}:{}:{}.log".format(today.year, today.month, today.day, today.hour,
                                                                 today.minute, today.second)
