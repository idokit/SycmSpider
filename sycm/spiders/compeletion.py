# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import Request, signals
from sycm.dto.ConfigData import ConfigData


class CompeletionSpider(scrapy.Spider):
    name = 'compeletion'
    allowed_domains = ['competition.com']
    start_urls = ['http://competition.com/']
    db_address = "mysql+mysqlconnector://root:123456@localhost:3306/test"

    def __init__(self, *args, **kwargs):
        super(CompeletionSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def start_requests(self):
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
        pass

    def closeSpider(self, spider):
        # self.browser.driver.quit()
        # self.db.close()
        pass
