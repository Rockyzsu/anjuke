# -*- coding: utf-8 -*-

# Scrapy settings for anjukecomm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'anjukecomm'

SPIDER_MODULES = ['anjukecomm.spiders']
NEWSPIDER_MODULE = 'anjukecomm.spiders'

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'test'
MONGODB_COLLECTION = 'anjuke'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'anjukecomm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'accept-language': 'zh,en;q=0.8,en-US;q=0.6', 'accept-encoding': 'gzip, deflate, br',
#  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'upgrade-insecure-requests': '1', 'referer': 'https://m.anjuke.com/ba/community/?from=anjuke_home',
# 'cookie': 'als=0; __xsptplus8=8.2.1503557877.1503557921.6%234%7C%7C%7C%7C%7C%23%23hWmIxvWGtBprdSupD-oChmF9MknKarey%23; lps="/|";#sessid=AA1DC8BC-375D-3025-4411-F1DE18A9495E; _ga=GA1.2.2091742266.1503400901; _gid=GA1.2.1006102639.1506599574; twe=2; #aQQ_ajkguid=AB109AF3-AAA3-9AEB-8739-7694D2BC3888; ctid=242; 58tj_uuid=32b49206-df0d-4ec8-abb6-b6befe305088; new_session=0; init_refer=; new_uv=4',
# 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

#   'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus)U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
#  'accept': 'text/html',
#  'accept-encoding': 'gzip, deflate, sdch',
# 'accept-language': 'zh-CN,zh;q=0.8',
# 'cache-control': 'no-cache',
# 'pragma': 'no-cache',
# 'x-requested-with': 'XMLHttpRequest',
# 'referer':'https://m.anjuke.com/ba/community/?from=anjuke_home'
#}
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'anjukecomm.middlewares.AnjukecommSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'anjukecomm.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'anjukecomm.pipelines.AnjukecommPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
ITEM_PIPELINES = {
'anjukecomm.pipelines.AnjukecommPipeline':300,
# 'lianjia.pipelines.MySQLStoreHouse':300,
}
