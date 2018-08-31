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
import re
from sycm.dto.ConfigData import ConfigData


class OverviewMiddlewares(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # 子交易排行
    sub_trade_tr = (By.CSS_SELECTOR, ".mod-child-cate-rank table thead th")
    sub_trade_tb = (By.CSS_SELECTOR, ".mod-child-cate-rank table tbody td")
    # 需要翻页？
    sub_total = (By.CSS_SELECTOR, ".ui-pagination-total")
    sub_next = (By.CSS_SELECTOR, ".ui-pagination-next")
    # 报表
    report_list = (By.CSS_SELECTOR, ".mod-cate-report .list")
    # 表头
    report_tr = (By.CSS_SELECTOR, ".mod-cate-report table thead th")
    # 数据
    report_tb = (By.CSS_SELECTOR, ".mod-cate-report tbody tr:nth-of-type(1) td")
    # 选项
    report_checkbox = (By.CSS_SELECTOR, ".mod-cate-report .checkbox")

    data_type = ("市场-行业大盘-子行业交易排行", "市场-行业大盘-行业报表")

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

        if not request.url.find('overview'):
            return None
        # 行业大盘
        spider.browser.driver.get(request.url)
        spider.browser.driver.refresh()
        time.sleep(1)
        selection = request.meta['cate']
        seller = request.meta['seller']
        crawl_date = request.meta['crawl_date']
        devcice = request.meta['devcice']
        dateType = request.meta['dateType']
        common_tr, common_tb, data_key = ConfigData.cateField(selection, crawl_date, dateType, devcice, seller)
        # 查找子交易排行数据
        sub_trade_tr = spider.browser.find_elements(*self.sub_trade_tr)
        sub_trade_tb = spider.browser.find_elements(*self.sub_trade_tb)
        sub_trade_tb = [sub_trade_tb[i:i + len(sub_trade_tr)] for i in
                        range(0, len(sub_trade_tb), len(sub_trade_tr))]
        # 分页 是否需要
        self.sub_trade_process(spider, sub_trade_tb, sub_trade_tr, common_tr, common_tb, data_key, crawl_date)
        try:
            total_text = spider.browser.quick_find_element(*self.sub_total).text
            total = int(re.findall('(\d+)', total_text)[0])
        except Exception as e:
            print(e)
            total = 1
        while total > 1:
            spider.browser.click_item(*self.sub_next)
            sub_trade_tb = spider.browser.find_elements(*self.sub_trade_tb)
            sub_trade_tb = [sub_trade_tb[i:i + len(sub_trade_tr)] for i in
                            range(0, len(sub_trade_tb), len(sub_trade_tr))]
            self.sub_trade_process(spider, sub_trade_tb, sub_trade_tr, common_tr, common_tb, data_key, crawl_date)
            total = total - 1
            # 数据处理
        # 点击报表
        spider.browser.click_item(*self.report_list)
        report_tr = list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tr)))
        report_tb = list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tb)))
        # 判断类目层级
        if selection['depth'] != 1:
            for index in [0, 2, 4, 5, 7, 9, 1, 3, 6, 8, 10, 11, 14, 12]:
                spider.browser.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tr)))[1:]

            for index in [1, 3, 6, 8, 10, 11, 13, 15, 16, 17, 12]:
                spider.browser.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tr)))[1:]
        else:
            for index in [0, 2, 4, 5, 7, 9, 1, 3, 6, 8, 10, 11, 14, 12]:
                spider.browser.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tr)))[1:]
            for index in [1, 3, 6, 8, 10, 11, 13, 12]:
                spider.browser.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, spider.browser.find_elements(*self.report_tr)))[1:]
        report_tb = [report_tb[i:i + len(report_tr)] for i in
                     range(0, len(report_tb), len(report_tr))]
        # 分页 是否需要
        self.report_process(spider, report_tb, report_tr, common_tr, common_tb, data_key, crawl_date)

        return HtmlResponse(url=spider.browser.driver.current_url, encoding="UTF-8",
                            request=request)

    def report_process(self, spider, sub_trade_tb, sub_trade_tr, common_tr, common_tb, data_key, crawl_date):
        for tb_val in sub_trade_tb:
            json_str = json.dumps(dict(zip(sub_trade_tr + common_tr,
                                           tb_val + common_tb)),
                                  ensure_ascii=False)
            spider.db.add(DataSource(**{
                'shop_name': '宝洁官方旗舰店',
                'data_type': self.data_type[1],
                'data_key': '^_^'.join(data_key + [tb_val[0]]),
                'value': json_str,
                'pt_name': '生意参谋',
                'start_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d"),
                'end_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d") + datetime.timedelta(1),
                'gmt_create': datetime.datetime.now()
            }))
            spider.db.commit()

    def sub_trade_process(self, spider, sub_trade_tb, sub_trade_tr, common_tr, common_tb, data_key, crawl_date):
        for tb_val in sub_trade_tb:
            json_str = json.dumps(dict(zip(
                                            list(map(lambda v: v.text, sub_trade_tr)) + common_tr,
                                           list(map(lambda v, y: y == 2 and v.get_attribute('value') or v.text, tb_val,
                                                    range(len(sub_trade_tr)))) + common_tb)),
                                  ensure_ascii=False)
            spider.db.add(DataSource(**{
                'shop_name': '宝洁官方旗舰店',
                'data_type': self.data_type[0],
                'data_key': '^_^'.join(data_key + [tb_val[0].text]),
                'value': json_str,
                'pt_name': '生意参谋',
                'start_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d"),
                'end_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d") + datetime.timedelta(1),
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
        # print('-------------------')

        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
