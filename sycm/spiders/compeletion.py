# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import Request, signals
from sycm.dto.ConfigData import ConfigData
from sycm.dto.Dto import Dto


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
        start_time = yesterday
        end_time = yesterday
        for device in [0, 2]:
            # 周期类型
            for dateType in ['day']:
                # 类目
                for cate in cates:
                    # 终端
                    for seller in [-1, 1]:
                        cateId = ConfigData.getCateId(cate)
                        # 市场大盘
                        url = "https://sycm.taobao.com/mc/mq/overview?cateFlag=0&cateId={}&dateRange={}&dateType={}&device={}&sellerType={}".format(
                            cateId, start_time + "%7c" + end_time, dateType, device, seller)
                        yield Request(url, meta={
                            'cate': cate,
                            'seller': seller,
                            'start_time': start_time,
                            'end_time':end_time,
                            'devcice': device,
                            'dateType': dateType,
                        }, callback=self.parse)

    def parse(self, response):
        pass

    def closeSpider(self, spider):
        pass
