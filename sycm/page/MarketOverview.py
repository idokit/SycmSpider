import json

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
    cate_cons_s = (By.CSS_SELECTOR, '#cateCons')
    cate_cons_tr_s = (By.CSS_SELECTOR, '#cateCons thead  th')
    cate_cons_tb_s = (By.CSS_SELECTOR, '#cateCons tbody td')
    cate_cons_total_s = (By.CSS_SELECTOR, '#cateCons .ant-pagination li')
    cate_cons_title_s = (By.CSS_SELECTOR, '#cateCons .oui-card-title')
    cateCons_next_page_s = (By.CSS_SELECTOR, '#cateCons .ant-pagination-next')

    # 卖家概况
    seller_profile_s = (By.CSS_SELECTOR, '.oui-card')

    table_s = (By.CSS_SELECTOR, 'table')

    # 表头 tr

    # 表格 tb

    # 总页数

    # 下一页

    # 数据类型

    def parse_page(self):
        self.driver.get(self.request.url)
        common_tr, common_tb, data_key = ConfigData.cateField(**self.request.meta)
        # cate_trend = self.find_element(*self.cate_trend_s)
        # title = self.find_element(*self.title_s).text
        # cate_trend_tr = list(map(lambda v: v.text, self.find_elements(*self.cate_trend_tr_s)))
        # cate_trend_tb = list(map(lambda v: v.text, self.find_elements(*self.cate_trend_tb_s)))
        # while True:
        #     try:
        #         self.find_element(*self.cate_trend_next_s)
        #         # 点击下一页
        #         self.click_item(*(By.CSS_SELECTOR, '#cateTrend .right'))
        #         # time.sleep(.5)
        #         cate_trend_tr = cate_trend_tr + list(
        #             map(lambda v: v.text, self.find_elements(*self.cate_trend_tr_s)))
        #         cate_trend_tb = cate_trend_tb + list(
        #             map(lambda v: v.text, self.find_elements(*self.cate_trend_tb_s)))
        #     except Exception as e:
        #         logger.info(e)
        #         break

        # self.db.data_process(shop_name, data_type, data_key, value, pt_name, start_time, end_time)

        # 数据处理
        try:
            cate_cons = self.quick_find_element(*self.cate_cons_s)

            cate_cons_total_li = self.find_elements(*self.cate_cons_total_s)
            cate_cons_total = int(cate_cons_total_li[len(cate_cons_total_li) - 2].text)
            cate_cons_tr = self.find_elements(*self.cate_cons_tr_s)
            cate_cons_tr = cate_cons_tr[:5]
            cate_cons_tb = self.find_elements(*self.cate_cons_tb_s)
            cate_cons_tb = [cate_cons_tb[i:i + 5] for i in range(int(len(cate_cons_tb) / 6))]
            cate_cons_tr_text = (lambda v: v.text, cate_cons_tr)
            key = cate_cons_tr_text + common_tr
            for tb_val in cate_cons_tb:
                cate_cons_tb_text = list(
                    map(lambda v, y: y == 0 and v.find_element(By.CSS_SELECTOR, 'a').text or
                                     (y == 3 or y == 4) and v.find_element(By.CSS_SELECTOR,
                                                                           '.alife-dt-card-common-table-sortable-value').text or
                                     v.text, tb_val, range(len(tb_val)))
                )
                value = json.dumps(dict(zip(key,cate_cons_tb_text+common_tb)))
                # self.db.data_process('店铺名', '行业构成', data_key+[cate_cons_tb_text[0]], value, '生意参谋', start_time, end_time)


                # value = list(map())


            # while total > 1:
            #     cate_cons_tr = cate_cons.find_elements(*self.cate_cons_tr_s)
            #     cate_cons_tr = cate_cons_tr[:5]
            #     cate_cons_tb = cate_cons.find_elements(*self.cate_cons_tb_s)
            #     cate_cons_tb = [cate_cons_tb[i:i + 5] for i in range(int(len(cate_cons_tb) / 6))]
            #     print('数据处理')
            #     total = total - 1
            # self.db.data_process(shop_name, data_type, data_key, value, pt_name, start_time, end_time)

        except Exception as e:
            logger.info('当前类目缺少行业构成' + str(e))
