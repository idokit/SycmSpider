# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import Request, signals
from scrapy_redis.spiders import RedisSpider

from sycm.dto.ConfigData import ConfigData
from sycm.dto.Dto import Dto


class CompeletionSpider(RedisSpider):
    name = 'compeletion'

    def __init__(self, *args, **kwargs):
        super(CompeletionSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.closeSpider, signals.spider_closed)


    def parse(self, response):
        pass

    def closeSpider(self, spider):
        pass
