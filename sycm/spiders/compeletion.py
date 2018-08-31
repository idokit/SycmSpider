# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import Request, signals
from selenium import webdriver
from sycm.page.NewLogin import NewLogin
from sycm.dto.Dto import Dto
from sycm.dto.ConfigData import ConfigData
from sycm.entity.TaskProgress import TaskProgress


class CompeletionSpider(scrapy.Spider):
    name = 'compeletion'
    allowed_domains = ['competition.com']
    start_urls = ['http://competition.com/']
    db_address = "mysql+mysqlconnector://root:123456@localhost:3306/test"

    def __init__(self, *args, **kwargs):
        # TODO 爬虫初始化
        super(CompeletionSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.closeSpider, signals.spider_closed)
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\zhouyi\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome("C:\crawl\chromedriver", 0, options)
        # TODO 爬虫登录
        browser = NewLogin(driver=driver)
        browser.login()
        self.browser = browser
        self.db = Dto(self.db_address)
        pass

    def start_requests(self):
        # TODO url拼接
        yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")
        cates = ConfigData().getFullCate()
        cates = filter(lambda v: v['depth'] == 1, cates)
        for device in [0]:
            for dateType in ['recent1']:
                for cate in cates:
                    for seller in [-1, 1]:
                        cateId = ConfigData.getCateId(cate)
                        url = "https://sycm.taobao.com/mq/industry/overview/overview.htm?cateId={}&dateRange={}&dateType={}&device={}&seller={}".format(
                            cateId, yesterday + "%7c" + yesterday, dateType, device, seller)
                        yield Request(url, meta={
                            'cate': cate,
                            'seller': seller,
                            'crawl_date': yesterday,
                            'devcice': device,
                            'dateType': dateType
                        }, callback=self.parse)

    def parse(self, response):
        print('done----------------------------')

    def closeSpider(self, spider):
        self.browser.driver.quit()
        self.db.close()
