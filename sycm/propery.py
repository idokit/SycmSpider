import datetime
import json
import re
import time
from multiprocessing import Pool

import requests

from sycm.dto.ConfigData import ConfigData
import pandas as pd

from sycm.dto.Dto import Dto
from multiprocessing import pool


class Rank(object):
    tr = ['排名', '属性值', '交易指数', '支付件数', '类别']

    re_partern = re.compile(
        r"cateId=(.*?)&dateRange=(\d{4}-\d{2}-\d{2})%7C(\d{4}-\d{2}-\d{2})&dateType=(.*?)&device=0&hotAttrType=0&propertyId=122216905&seller=(.*?)$")

    db = Dto(sql_address='mysql+mysqlconnector://py_sycm:Kdi*33lSI@120.55.113.9:3306/toothpick')

    cates_items = ConfigData().get_all()

    @classmethod
    def run(cls):
        url = "https://sycm.taobao.com/mq/property/hotRank.json?" \
              "cateId={cateId}&dateRange={start_time}%7C{end_time}&dateType={dateType}&device=0&hotAttrType=0&propertyId=122216905&seller={seller}"
        dateType = 'day'
        sellers = [-1, 0, 1]
        crawl_dates = [[v.strftime('%Y-%m-%d'), v.strftime('%Y-%m-%d')] for v in
                       pd.date_range('2018-06-20', '2018-09-16').date]
        arr = []
        for cateId in [121484013, 121422013, 121468012, 121368013, 121452007, 121396013]:
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
        print(commom_tr)
        print(common_tb)
        print(data_key)
        data = []
        try:
            time.sleep(1)
            data = cls.request(url)
        except Exception as e:
            print(e)
        if data:
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
                               'cookie': 'cookie2=19b3cf1a61b5e088b1f21ca683995e05; csg=4586600b'
                           })
        if rep.status_code == 200:
            rep_josn = json.loads(rep.text, encoding='utf-8')
            if rep_josn['hasError'] == False:
                return rep_josn['content']['data']['data']
        else:
            print(rep.text)
            return []

    @classmethod
    def parse(cls, data, common_tr, common_tb, data_key, start_time, end_time):
        for tb in data:
            tb = [tb['rank'], tb['properties'][0]['value']['name'], tb['tradeIndex'], tb['payItemQty'],
                  tb['properties'][0]['name']]
            try:
                json_str = json.dumps(dict(zip(cls.tr + common_tr, tb + common_tb)), ensure_ascii=False)
                cls.db.data_process(
                    '宝洁官方旗舰', '市场行情-属性分析-属性排行-热销属性榜', data_key + [str(tb[0])], json_str, '百雀羚旗舰店', start_time, end_time
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
