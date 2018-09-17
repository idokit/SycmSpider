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
        # options = webdriver.ChromeOptions()
        # options.add_argument(r"user-data-dir=C:\Users\zhouyi\AppData\Local\Google\Chrome\User Data")
        # options.add_argument(r"user-data-dir=C:\Users\pc\AppData\Local\Google\Chrome\User Data")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(r"C:\crawl\chromedriver", 0, options)
        # self.driver = Login(driver=driver).login()
        # self.db = Dto("mysql+mysqlconnector://root:123456@localhost:3306/test")
        # self.cates = ConfigData().get_all()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.close, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # if request.url.startswith('https://sycm.taobao.com/mc/mq/overview'):
        #     Page = importlib.import_module('sycm.page.MarketOverview').Page
        #     page = Page(driver=self.driver, request=request, db=self.db, cates=self.cates)
        #     # page.parse_page()
        #     # url = 'https://i.taobao.com/my_taobao.htm'
        #     s.get('https://i.taobao.com/my_taobao.htm')
        # # else:
        # #     logger.error('url无法找到对应的处理页面' + request.url)
        # print(request.url)
        # return HtmlResponse(url=request.url, encoding="UTF-8",
        #                     request=request)
        request.cookies = {
            'cookie2': "1cf1da182b8b5efe7aa0a55586b0e808"
        }
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def close(self):
        # 关闭
        # self.driver.close()
        # self.db.close()
        pass
