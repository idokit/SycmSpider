# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_redis.spiders import RedisSpider


class CompeletionSpider(Spider):
    name = 'compeletion'

    def __init__(self, *args, **kwargs):
        super(CompeletionSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url="https://sycm.taobao.com/ucc/mc/notify/listNotify.json?groupCode=one_plat",callback=self.parse)


    def parse(self, response):
        print(response.text)
        pass

    def closeSpider(self, spider):
        pass
