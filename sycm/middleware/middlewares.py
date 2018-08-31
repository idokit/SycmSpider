# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
import time
import datetime
from sycm.entity.DataSource import DataSource
import json


class SycmDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    common_table = '{} .ebase-Table__table {}'

    _data_type = ((
                      "#competeShop-competeShopList", "竞店榜"
                  ), (
                      "#competeShop-competeShopItem", "竞店商品榜"
                  ), (
                      "#competeShop-competeShopSrcCpr", "竞店入店来源对比"
                  ), (
                      "#competeShop-competeShopSwCpr", "竞店入店关键词对比"
                  )
    )

    def scroll_bottom(self, spider):
        try:
            spider.browser.script("window.scroll(0,document.querySelector('.ebase-Footer__root').offsetTop)")
        except Exception as e:
            print(e)
            self.scroll_bottom(spider)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called


        if not request.url.find('summary'):
            return None
        spider.browser.driver.get(request.url)
        time.sleep(1)
        for items in self._data_type:
            spider.browser.click_item(By.CSS_SELECTOR, items[0] + " .oui-select-container-frame")
            drop_down = spider.browser.find_elements(By.CSS_SELECTOR, ".oui-dropdown .oui-dropdown-item")
            terminal_len = len(drop_down)
            spider.browser.script(
                "document.querySelectorAll(%r)[%r].click()" % (".oui-dropdown .oui-dropdown-item", 0))
            for i in range(terminal_len):
                item = spider.browser.click_item(By.CSS_SELECTOR, items[0] + " .oui-select-container-frame")
                print(item.text)
                spider.browser.script(
                    "document.querySelectorAll(%r)[%r].click()" % (".oui-dropdown .oui-dropdown-item", i))
                time.sleep(1)
                spider.browser.script(
                    "document.querySelectorAll('%s .oui-pagination-items span')[%r].click()" % (items[0], 0))
                tb = spider.browser.find_elements(By.CSS_SELECTOR, items[0] + " tbody td")
                tr = spider.browser.find_elements(By.CSS_SELECTOR, items[0] + " thead th")
                tb = [tb[i:i + (len(tr))] for i in range(0, len(tb), len(tr))]
                total = spider.browser.find_elements(By.CSS_SELECTOR, items[0] + " .oui-pagination-items span")
                total = int(total[len(total) - 1].text)
                self.data_process(items[1], tr, tb, spider)
                while total > 1:
                    spider.browser.click_item(By.CSS_SELECTOR, items[0] + " .oui-pagination-next")
                    tr = spider.browser.find_elements(By.CSS_SELECTOR, items[0] + " thead th")
                    tb = spider.browser.find_elements(By.CSS_SELECTOR, items[0] + " tbody td")
                    tb = [tb[i:i + (len(tr))] for i in range(0, len(tb), len(tr))]
                    total = total - 1
                    self.data_process(items[1], tr, tb, spider)

        return HtmlResponse(url=spider.browser.driver.current_url, encoding="UTF-8",
                            request=request)

    def data_process(self, data_type, tr, tb, spider):
        for tb_val in tb:
            spider.db.add(DataSource(**{
                'shop_name': '宝洁',
                'data_type': data_type,
                'data_key': 'data_key',
                'value': json.dumps(dict(zip(map(lambda v: v.text, tr), map(lambda v: v.text, tb_val))),
                                    ensure_ascii=False),
                'pt_name': '平台名',
                'start_time': datetime.datetime.now(),
                'end_time': datetime.datetime.now() + datetime.timedelta(1),
                'gmt_create': datetime.datetime.now()
            }))
        spider.db.commit()

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        print('-------------------')
        pass


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
