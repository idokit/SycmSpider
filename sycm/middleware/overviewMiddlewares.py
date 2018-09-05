# -*- coding: utf-8 -*-
import re

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import importlib
import logging

from sycm.dto.ConfigData import ConfigData
from sycm.dto.Dto import Dto
from sycm.page.Login import Login

logger = logging.getLogger(__name__)


class OverviewMiddlewares(object):
    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\zhouyi\AppData\Local\Google\Chrome\User Data")
        # options.add_argument(r"user-data-dir=C:\Users\pc\AppData\Local\Google\Chrome\User Data")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(r"C:\crawl\chromedriver", 0, options)
        # self.driver = Login(driver=driver).login()
        # self.db = Dto("mysql+mysqlconnector://root:123456@localhost:3306/test")
        self.cates = ConfigData().get_all()
        self.re_reg = re.compile(
            r"cateId=(.*?)&dateRange=(\d{4}-\d{2}-\d{2})%7c(\d{4}-\d{2}-\d{2})&dateType=(.*?)&device=(.*?)&sellerType=(.*?)$")

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # if True:
        #     Page = importlib.import_module('sycm.page.MarketOverview').Page
        # page = Page(driver=self.driver, request=request, db=self.db,cates = self.cates)
        # page.parse_page()
        [(cate, start_time, end_time, dateType, devcice, seller)] = self.re_reg.findall(request.url)
        print(ConfigData.cateField(self.cates, cate, start_time, end_time, dateType, devcice, seller))
        return HtmlResponse(url=request.url, encoding="UTF-8",
                            request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        logger.error('处理异常')
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
