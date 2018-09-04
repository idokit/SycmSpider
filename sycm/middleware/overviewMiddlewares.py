# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import importlib
import logging

from sycm.dto.Dto import Dto
from sycm.page.Login import Login

logger = logging.getLogger(__name__)


class OverviewMiddlewares(object):
    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\zhouyi\AppData\Local\Google\Chrome\User Data")
        driver = webdriver.Chrome(r"C:\crawl\chromedriver", 0, options)
        self.driver = Login(driver=driver).login()
        self.db = Dto("mysql+mysqlconnector://root:123456@localhost:3306/test")

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if True:
            Page = importlib.import_module('sycm.page.MarketOverview').Page
        page = Page(driver=self.driver, request=request, db=self.db)
        page.parse_page()
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
