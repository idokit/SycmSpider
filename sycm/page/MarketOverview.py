from selenium.webdriver.common.by import By

from sycm.dto.ConfigData import ConfigData
from sycm.page.Base import Base
import logging

logger = logging.getLogger(__name__)


class Page(Base):
    # 行业趋势
    cate_trend_s = (By.CSS_SELECTOR, '#cateTrend')
    cate_trend_tr_s = (By.CSS_SELECTOR, '.oui-index-cell-indexName')
    cate_trend_tb_s = (By.CSS_SELECTOR, '.oui-index-cell-indexValue')
    cate_trend_next_s = (By.CSS_SELECTOR, '.right')

    # 行业构成
    cate_cons_s = (By.CSS_SELECTOR, '#cateCons')

    # 卖家概况
    seller_profile_s = (By.CSS_SELECTOR, '.oui-card')

    table_s = (By.CSS_SELECTOR, 'table')

    # 表头 tr
    tr_s = (By.CSS_SELECTOR, 'thead  th')
    # 表格 tb
    tb_s = (By.CSS_SELECTOR, 'tbody td')
    # 总页数
    total_s = (By.CSS_SELECTOR, '.ant-pagination li')
    # 下一页
    cateCons_next_page_s = (By.CSS_SELECTOR, '#cateCons .ant-pagination-next')
    # 数据类型
    title_s = (By.CSS_SELECTOR, '.oui-card-title')

    def parse_page(self):
        self.driver.get(self.request.url)
        # 获取通用tr tb
        common_tr, common_tb, data_key = ConfigData.cateField(**self.request.meta)
        cate_trend = self.find_element(*self.cate_trend_s)
        title = cate_trend.find_element(*self.title_s).text
        cate_trend_tr = list(map(lambda v: v.text, cate_trend.find_elements(*self.cate_trend_tr_s)))
        cate_trend_tb = list(map(lambda v: v.text, cate_trend.find_elements(*self.cate_trend_tb_s)))
        while True:
            try:
                cate_trend.find_element(*self.cate_trend_next_s)
                # 点击下一页
                self.click_item(*(By.CSS_SELECTOR, '#cateTrend .right'))
                # time.sleep(.5)
                cate_trend_tr = cate_trend_tr + list(
                    map(lambda v: v.text, cate_trend.find_elements(*self.cate_trend_tr_s)))
                cate_trend_tb = cate_trend_tb + list(
                    map(lambda v: v.text, cate_trend.find_elements(*self.cate_trend_tb_s)))
            except Exception as e:
                logger.info(e)
                break

        # self.db.data_process(shop_name, data_type, data_key, value, pt_name, start_time, end_time)

        # 数据处理
        try:
            title = ''
            cate_cons = self.quick_find_element(*self.cate_cons_s)
            # total
            total_li = cate_cons.find_elements(*self.total_s)
            total = int(total_li[len(total_li) - 2].text)
            cate_cons_tr = cate_cons.find_elements(*self.tr_s)
            cate_cons_tr = cate_cons_tr[:5]
            cate_cons_tb = cate_cons.find_elements(*self.tb_s)
            cate_cons_tb = [cate_cons_tb[i:i + 5] for i in range(int(len(cate_cons_tb) / 6))]
            for tb in cate_cons_tb:
                value = list(map())
                # self.db.data_process(shop_name, data_type, data_key, value, pt_name, start_time, end_time)
            while total > 1:
                cate_cons_tr = cate_cons.find_elements(*self.tr_s)
                cate_cons_tr = cate_cons_tr[:5]
                cate_cons_tb = cate_cons.find_elements(*self.tb_s)
                cate_cons_tb = [cate_cons_tb[i:i + 5] for i in range(int(len(cate_cons_tb) / 6))]
                print('数据处理')
                total = total - 1
                # self.db.data_process(shop_name, data_type, data_key, value, pt_name, start_time, end_time)
        except Exception as e:
            logger.info('当前类目缺少行业构成' + str(e))




