import datetime
import json
import re
import time
from enum import Enum
from multiprocessing import Pool

import requests

from sycm.dto.ConfigData import ConfigData
import pandas as pd

from sycm.dto.Dto import Dto
from multiprocessing import pool


class ItenEnum(Enum):
    uv = "访客数"
    pv = "浏览量"
    searchUvCnt = "搜索点击人数"
    searchPvCnt = "搜索点击次数"
    searchClkRate = "搜索点击率"
    favBuyerCnt = "收藏人数"
    favCnt = "收藏次数"
    addCartBuyerCnt = "加购人数"
    addCartCnt = "加购次数"
    payPct = "客单价"
    visitItemCnt = "浏览商品数"
    sellerCnt = "卖家数"
    visitSellerCnt = "被浏览卖家数"
    paySellerCnt = "被支付卖家数"
    payItemQty = "支付件数"
    searchIndex = "搜索人气"
    tradeIndex = "交易指数"
    payAmtParentRate = "支付金额较父类目占比"


class Rank(object):
    re_partern = re.compile(
        r"cateId=(.*?)&dateRange=(\d{4}-\d{2}-\d{2})%7C(\d{4}-\d{2}-\d{2})&dateType=(.*?)&device=0&indexCode=uv\|pv\|searchUvCnt\|searchPvCnt\|searchClkRate\|favBuyerCnt\|favCnt\|addCartBuyerCnt\|addCartCnt\|payPct\|visitItemCnt\|sellerCnt\|visitSellerCnt\|paySellerCnt\|payItemQty\|searchIndex\|tradeIndex\|payAmtParentRate&seller=(.*?)$")

    db = Dto(sql_address='mysql+mysqlconnector://py_sycm:Kdi*33lSI@120.55.113.9:3306/toothpick')

    cates_items = ConfigData().get_all()


    @classmethod
    def run(cls):
        url = \
            "https://sycm.taobao.com/mq/overview/reportIndex.json?cateId={cateId}&dateRange={start_time}%7C{end_time}&dateType={dateType}&device=0&indexCode=uv|pv|searchUvCnt|searchPvCnt|searchClkRate|favBuyerCnt|favCnt|addCartBuyerCnt|addCartCnt|payPct|visitItemCnt|sellerCnt|visitSellerCnt|paySellerCnt|payItemQty|searchIndex|tradeIndex|payAmtParentRate&seller={seller}"
        cates = ConfigData().getFullCate()

        print(cates)
        dateType = 'month'
        sellers = [1,-1]
        crawl_dates = [[datetime.date(v.year, v.month, 1).strftime('%Y-%m-%d'), v.strftime('%Y-%m-%d')] for v in
                       pd.date_range('2015-09-01', '2018-09-01', freq='1M').date]
        arr = []
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
                    arr.append(new_url)
                    print(new_url)
        return arr

    @classmethod
    def worker(cls, url):
        (cateId, start_time, end_time, dateType, seller) = cls.re_partern.findall(url)[0]
        commom_tr, common_tb, data_key = ConfigData.cateField(cls.cates_items, cateId, start_time, end_time, dateType,
                                                              0, seller)
        data = []

        if  int(cateId) == 1801 or int(cateId) == 50010788:
            url = "https://sycm.taobao.com/mq/overview/reportIndex.json?cateId={cateId}&dateRange={start_time}%7C{end_time}&dateType={dateType}&device=0&indexCode=uv|pv|searchUvCnt|searchPvCnt|searchClkRate|favBuyerCnt|favCnt|addCartBuyerCnt|addCartCnt|payPct|visitItemCnt|sellerCnt|visitSellerCnt|paySellerCnt|payItemQty&seller={seller}".format(
                cateId=cateId,
                start_time=start_time,
                end_time=end_time,
                dateType=dateType,
                seller=seller
            )
        try:
            data = cls.request(url)
        except Exception as e:
            print(e)
        if len(data)!=0:
            cls.parse(data, commom_tr, common_tb, data_key, start_time, end_time)

    @classmethod
    def request(cls, new_url):
        rep = requests.get(new_url,
                           headers={
                               'Connection': 'keep-alive',
                               'Cache-Control': 'max-age=0',
                               'Accept': '/',
                               'Upgrade-Insecure-Requests': '1',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                               'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': 'zh-CN,zh;q=0.8',
                               'cookie': 'cookie2=19b3cf1a61b5e088b1f21ca683995e05; csg=471e903e'
                           })
        if rep.status_code == 200:
            rep_josn = json.loads(rep.text, encoding='utf-8')
            if rep_josn['hasError'] == False:
                return rep_josn['content']['data']
        else:
            print(rep.text)
            return []

    @classmethod
    def parse(cls, data, common_tr, common_tb, data_key, start_time, end_time):
        tr = [ItenEnum[v['indexCode']].value for v in data]
        tb = [v.get('currentValue',None) for v in data]
        try:
            json_str = json.dumps(dict(zip(tr + common_tr, tb + common_tb)), ensure_ascii=False)
            cls.db.data_process(
                '宝洁官方旗舰', '市场行情-行业大盘-行业报表', data_key + [start_time], json_str, '百雀羚旗舰店', start_time, end_time
            )
            print(json_str)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    urls = Rank.run()
    time_start = time.time()
    pool = Pool()  # 创建4个进程
    pool.map(Rank.worker, urls)
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()

    time_end = time.time()

    print('totally cost', time_end - time_start)



