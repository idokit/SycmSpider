import json
import time

from selenium.webdriver.common.by import By

from sycm.dto.ConfigData import ConfigData
from sycm.page.Base import Base
import logging

logger = logging.getLogger(__name__)


class Page(Base):
    # 行业趋势
    cate_trend_s = (By.CSS_SELECTOR, '#cateTrend')
    cate_trend_tr_s = (By.CSS_SELECTOR, '#cateTrend .oui-index-cell-indexName')
    cate_trend_tb_s = (By.CSS_SELECTOR, '#cateTrend .oui-index-cell-indexValue')
    cate_trend_next_s = (By.CSS_SELECTOR, '#cateTrend .right')

    # 行业构成
    tr_s = '{} thead  th'
    tb_s = '{} tbody td'
    total_s = '{} .ant-pagination li'
    title_s = '{} .oui-card-title'
    next_page_s = '{} .ant-pagination-next'

    total_table = (('#cateCons','市场-市场大盘-行业构成'), ('#cateOverview','市场-市场大盘-卖家概况-子行业分布'), ('#mc-mq-map-table-table','市场-市场大盘-卖家概况-地域分布'))

    def parse_page(self):
        self.driver.get(self.request.url)
        self.driver.refresh()
        time.sleep(2)
        common_tr, common_tb, data_key = ConfigData.cateField(**self.request.meta)
        cate_trend_tr = list(map(lambda v: v.text, self.find_elements(*self.cate_trend_tr_s)))
        cate_trend_tb = list(map(lambda v: v.text, self.find_elements(*self.cate_trend_tb_s)))
        while True:
            try:
                self.quick_find_element(*self.cate_trend_next_s)
                self.click_item(*(By.CSS_SELECTOR, '#cateTrend .right'))
                cate_trend_tr = cate_trend_tr + list(
                    map(lambda v: v.text, self.find_elements(*self.cate_trend_tr_s)))
                cate_trend_tb = cate_trend_tb + list(
                    map(lambda v: v.text, self.find_elements(*self.cate_trend_tb_s)))
            except Exception as e:
                logger.info(e)
                break
        value = json.dumps(dict(zip(cate_trend_tr + common_tr, cate_trend_tb + common_tb))
                           , ensure_ascii=False)
        self.db.data_process('店铺名', '市场-市场大盘-行业趋势', data_key + [cate_trend_tb[0]], value, '生意参谋',
                             self.request.meta['start_time'], self.request.meta['end_time'])

        for table in self.total_table:
            try:
                current_table = self.quick_find_element(By.CSS_SELECTOR, table[0])
            except Exception as e:
                logger.info(e)
                continue

            self.process(table, common_tb, common_tr, data_key)
            total = self.find_elements(By.CSS_SELECTOR, self.total_s.format(table[0]))
            total = int(total[len(total) - 2].text)
            while total > 1:
                self.click_item(By.CSS_SELECTOR, self.next_page_s.format(table[0]))
                self.process(table, common_tb, common_tr, data_key)
                total = total - 1

    def process(self, table, common_tb, common_tr, data_key):
        tr = self.find_elements(By.CSS_SELECTOR, self.tr_s.format(table[0]))
        tb = self.find_elements(By.CSS_SELECTOR, self.tb_s.format(table[0]))
        tb = [tb[i:i + len(tr)] for i in range(0, len(tb), len(tr))]
        key = list(map(lambda v: v.text, tr)) + common_tr
        for tb_item in tb:
            tb_val = list(map(lambda v: v.text.split('\n')[0] or v.text, tb_item))
            value = json.dumps(dict(zip(key, tb_val + common_tb)), ensure_ascii=False)
            self.db.data_process('宝洁官方旗舰店', table[1], data_key + [tb_val[0]], value, '生意参谋',
                                 self.request.meta['start_time'], self.request.meta['end_time'])
