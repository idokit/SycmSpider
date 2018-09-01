# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import importlib
import logging

logger = logging.getLogger(__name__)


class OverviewMiddlewares(object):
    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\zhouyi\AppData\Local\Google\Chrome\User Data")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(r"C:\crawl\chromedriver", 0, options)
        # 登录
        Page = importlib.import_module('sycm.page.Compeletion').Page
        self.page = Page(driver=self.driver)
        self.page.login()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if not request.url.find('overview'):
            return None
        self.page.parse_page(request=request)
        return HtmlResponse(url=request.url, encoding="UTF-8",
                            request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        logger.error('处理异常')
        logger.error(exception)
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
