import datetime
import json
import time

import requests

from sycm.dto.ConfigData import ConfigData
import pandas as pd

from sycm.dto.Dto import Dto


class Rank(object):
    tr = ['热销排名', '品牌名称', '交易指数', '交易增长幅度', '支付商品数', '支付转化率', '品牌ID']

    item = ['rankNo', 'brandName', 'tradeIndex', 'tradeIndexPercent', 'payItemCnt', 'payByrRate', 'brandId']

    def __init__(self):
        self.db = Dto(sql_address='mysql+mysqlconnector://py_sycm:Kdi*33lSI@120.55.113.9:3306/toothpick')

    def run(self):
        url = "https://sycm.taobao.com/mq/brand/rank.json?" \
              "cateId={cateId}&" \
              "dateRange={start_time}%7C{end_time}&" \
              "dateType={dateType}&device=0&orderField=tradeIndex&orderType=desc&page=1&pageSize=10&rankType=0&search=&seller={seller}"
        # 获取所有类目
        dateType = 'month'
        sellers = [-1, 0, 1]
        crawl_dates = [[datetime.date(v.year, v.month, 1).strftime('%Y-%m-%d'), v.strftime('%Y-%m-%d')] for v in
                       pd.date_range('2017-08-01', '2018-09-01', freq='1M').date]

        self.all = ConfigData().get_all()
        cates_items = self.all
        cates = [ 50011991,50011992,121366011,121408009,125172008]
        for cateId in cates:
            for crawl_date in crawl_dates:
                for seller in sellers:
                    new_url = url.format(
                        cateId=cateId,
                        start_time=crawl_date[0],
                        end_time=crawl_date[1],
                        dateType=dateType,
                        seller=seller
                    )
                    print(new_url)
                    commom_tr, common_tb, data_key = ConfigData.cateField(cates_items, cateId, crawl_date[0],
                                                                          crawl_date[1],
                                                                          dateType, 0, seller)
                    data = []
                    try:
                        data = self.request(new_url)
                    except Exception as e:
                        print(e)
                    if data:
                        self.parse(data, commom_tr, common_tb, data_key, crawl_date[0], crawl_date[1])

    def request(self, new_url):
        rep = requests.get(new_url,
                           headers={
                               'Connection': 'keep-alive',
                               'Cache-Control': 'max-age=0',
                               'Accept': '/',
                               'Upgrade-Insecure-Requests': '1',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                               'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': 'zh-CN,zh;q=0.8',
                               'cookie': 'cookie2=11242a80535c6ef9915c6475bdb86496; csg=993f274e'
                           })
        if rep.status_code == 200:
            rep_josn = json.loads(rep.text, encoding='utf-8')
            if rep_josn['hasError'] == False:
                return rep_josn['content']['data']['data']
        else:
            print(rep.text)
            return []

    def parse(self, data, common_tr, common_tb, data_key, start_time, end_time):
        count = 0
        for tbs in data:
            count += 1
            if count > 50:
                break
            tb = [tbs.get(key, None) for key in self.item]
            try:
                json_str = json.dumps(dict(zip(self.tr + common_tr, tb + common_tb)), ensure_ascii=False)
                self.db.data_process(
                    '宝洁官方旗舰', '品牌分析-品牌排行-热销品牌榜', data_key + [str(tb[0])], json_str, '百雀羚旗舰店', start_time, end_time
                )
                print(json_str)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    Rank().run()
