# Scrapy settings for posbenchmark project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "posbenchmark"

SPIDER_MODULES = ["posbenchmark.spiders"]
NEWSPIDER_MODULE = "posbenchmark.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "posbenchmark (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "posbenchmark.middlewares.PosbenchmarkSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "posbenchmark.middlewares.PosbenchmarkDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "posbenchmark.pipelines.PosbenchmarkPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Enable Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Configure Playwright to use headless mode
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to False for debugging
    "timeout": 60 * 1000,  # Timeout in milliseconds
    "slow_mo": 50, # Slow down actions
    # "logger": {"level": "INFO", "name": "playwright"}, # Enable Playwright logs
}

# Set a reasonable concurrency for Playwright requests
CONCURRENT_REQUESTS = 10
PLAYWRIGHT_MAX_CONTEXTS = 5
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 5

# Avoid getting blocked by setting realistic delays
DOWNLOAD_DELAY = 3
RANDOM_DELAY= 1
# RETRY_TIMES = 3  # Retry 3 times
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 429]  # Retry these status codes
# Enable logging for debugging (optional)
LOG_LEVEL = "INFO"
CLOSESPIDER_TIMEOUT = 180 # Stop after 60 seconds

DOWNLOADER_MIDDLEWARES = {
   'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
   'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ROTATING_PROXY_LIST = [
    '185.200.38.98:1080',
    '95.9.218.176:3310'
    # ücretli ya da güvenilir proxy’leri buraya ekle
]

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'


# DEFAULT_REQUEST_HEADERS = {
#     'cookie': 'prov=4568ad3a-2c02-1686-b062-b26204fd5a6a; usr=p=%5b10%7c15%5d%5b160%7c%3bNewest%3b%5d',
#     'referer': 'https://www.google.com/',
#     # Add more custom headers as needed
# }
