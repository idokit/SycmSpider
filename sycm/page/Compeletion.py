import re
import time
from selenium.webdriver.common.by import By

from sycm.page.Base import Base


class Page(Base):
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
            self.script("window.scroll(0,document.querySelector('.ebase-Footer__root').offsetTop)")
        except Exception as e:
            print(e)
            self.scroll_bottom(spider)

    def __init(self, *args, **kw):
        super(Page, self).__init__(*args, **kw)

    def report_process(self, spider, sub_trade_tb, sub_trade_tr, common_tr, common_tb, data_key, crawl_date):
        pass
        # for tb_val in sub_trade_tb:
        #     json_str = json.dumps(dict(zip(sub_trade_tr + common_tr,
        #                                    tb_val + common_tb)),
        #                           ensure_ascii=False)
        #     spider.db.add(DataSource(**{
        #         'shop_name': '宝洁官方旗舰店',
        #         'data_type': self.data_type[1],
        #         'data_key': '^_^'.join(data_key + [tb_val[0]]),
        #         'value': json_str,
        #         'pt_name': '生意参谋',
        #         'start_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d"),
        #         'end_time': datetime.datetime.strptime(crawl_date, "%Y-%m-%d") + datetime.timedelta(1),
        #         'gmt_create': datetime.datetime.now()
        #     }))
        #     spider.db.commit()

    def sub_trade_process(self):
        pass

    def parse_page(self):
        self.driver.get(self.request.url)
        # self.driver.refresh()
        # common_tr, common_tb, data_key = ConfigData.cateField(selection, crawl_date, dateType, devcice, seller)
        sub_trade_tr = self.find_elements(*self.sub_trade_tr)
        sub_trade_tb = self.find_elements(*self.sub_trade_tb)
        sub_trade_tb = [sub_trade_tb[i:i + len(sub_trade_tr)] for i in
                        range(0, len(sub_trade_tb), len(sub_trade_tr))]
        # 分页 是否需要
        self.sub_trade_process()
        try:
            total_text = self.quick_find_element(*self.sub_total).text
            total = int(re.findall('(\d+)', total_text)[0])
        except Exception as e:
            print(e)
            total = 1
        while total > 1:
            self.click_item(*self.sub_next)
            sub_trade_tb = self.find_elements(*self.sub_trade_tb)
            sub_trade_tb = [sub_trade_tb[i:i + len(sub_trade_tr)] for i in
                            range(0, len(sub_trade_tb), len(sub_trade_tr))]
            self.sub_trade_process()
            total = total - 1
        # 点击报表
        self.click_item(*self.report_list)
        report_tr = list(map(lambda v: v.text, self.find_elements(*self.report_tr)))
        report_tb = list(map(lambda v: v.text, self.find_elements(*self.report_tb)))
        # 判断类目层级
        if True:
            for index in [0, 2, 4, 5, 7, 9, 1, 3, 6, 8, 10, 11, 14, 12]:
                self.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, self.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, self.find_elements(*self.report_tr)))[1:]

            for index in [1, 3, 6, 8, 10, 11, 13, 15, 16, 17, 12]:
                self.click_items(index, *self.report_checkbox)
            time.sleep(1)
            report_tb = report_tb + list(map(lambda v: v.text, self.find_elements(*self.report_tb)))[1:]
            report_tr = report_tr + list(map(lambda v: v.text, self.find_elements(*self.report_tr)))[1:]
        # else:
        #     for index in [0, 2, 4, 5, 7, 9, 1, 3, 6, 8, 10, 11, 14, 12]:
        #         self.click_items(index, *self.report_checkbox)
        #     time.sleep(1)
        #     report_tb = report_tb + list(map(lambda v: v.text, self.find_elements(*self.report_tb)))[1:]
        #     report_tr = report_tr + list(map(lambda v: v.text, self.find_elements(*self.report_tr)))[1:]
        #     for index in [1, 3, 6, 8, 10, 11, 13, 12]:
        #         self.click_items(index, *self.report_checkbox)
        #     time.sleep(1)
        #     report_tb = report_tb + list(map(lambda v: v.text, self.find_elements(*self.report_tb)))[1:]
        #     report_tr = report_tr + list(map(lambda v: v.text, self.find_elements(*self.report_tr)))[1:]
        # report_tb = [report_tb[i:i + len(report_tr)] for i in
        #              range(0, len(report_tb), len(report_tr))]
        self.report_process()

    def data_process(self):
        pass
