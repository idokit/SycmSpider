# 生成要爬取的链接
import datetime
import json
import re

from sycm.dto.ConfigData import ConfigData
from sycm.util.RedisClient import RedisClient
import pandas as pd
import requests
from sycm.dto.Dto import Dto


def main():
    db = RedisClient('127.0.0.1', '6379')
    cates = ConfigData().getFullCate(needJunjor=False)
    crawl_dates = [['2018-08-12', '2018-09-10']]

    deo = Dto("mysql+mysqlconnector://root:123456@localhost:3306/test")
    urls = [
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getJob.json?age=&area=&cateId={}&dateRange=2018-08-12|2018-09-10&dateType=recent30"
                   "&device=0&price={}&seller={}&sex=",
            "name": "职业分布"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getLevel.json?age=&area=&cateId={}&dateRange=2018-08-12|2018-09-10&"
                   "dateType=recent30&device=0&price={}&seller={}&sex=",
            "name": "淘气值分布"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getBuyerArea.json?age=&area=&areaType=province&cateId={}&currentPage=1&"
                   "dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&pageSize=10&price={}&seller={}&sex=",
            "name": "省份分布排行"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getBuyerArea.json?age=&area=&areaType=city&cateId={}"
                   "&currentPage=1&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&pageSize=10&price={}&seller={}&sex=",
            "name": "城市分布排行"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getFondnessPropsByOneLevel.json?age=&area=&"
                   "cateId={}&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&price={}&seller={}&sex=",
            "name": "属性偏好"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getKeyWord.json?age=&area=&cateId={}&dateRange=2018-08-12|2018-09-10&"
                   "dateType=recent30&device=0&price={}&seller={}&sex=",
            "name": "搜索词偏好"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getNinetyDaysBuyCnt.json?age=&area=&cateId={}&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&price={}&seller={}&sex=",
            "name": "近90天购买次数"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getNinetyDaysAmt.json?age=&area=&cateId={}&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&price={}&seller={}&sex=",
            "name": "近90天支付金额"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getFondnessBrand.json?age=&area=&cateId={}&currentPage=1&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&pageSize=10&preference=brand&price={}&seller={}&sex=",
            "name": "买家品牌购买偏好"
        },
        {
            "url": "sycm.taobao.com/mq/buyerPortrait/getFondnessBrand.json?age=&area=&cateId={}&currentPage=1&dateRange=2018-08-12|2018-09-10&dateType=recent30&device=0&pageSize=10&preference=cate&price={}&seller={}&sex=",
            "name": "买家类目购买偏好"
        }
    ]
    # 数据类型
    for url in urls:
        for cate in [50010788, 1801]:
            price_list = []
            if cate == 50010788:
                price_list = [('', '全部'), ('0-25', 0.3995), ('25-55', 0.3059), ('55-120', '0.1999'),
                              ('120-235', 0.0597), ('235-360', 0.0247), ('360', 0.0103)]
            elif cate == 1801:
                price_list = [('', '全部'), ('0-30', 0.2950), ('30-65', 0.3088), ('65-135', 0.2454), ('135-240', 0.0928),
                              ('240-450', 0.0383), ('405', 0.0197)]

            for price in price_list:
                for seller in [-1, 0, 1]:
                    # 终端
                    new_url = url['url'].format(cate, price[0], seller)
                    # res = url_reader(new_url)
                    # print('============')
                    # json.loads(,encoding='utf-8')

                    # deo.data_process('宝洁官方旗舰店', '市场-市场行情-买家人群', '', value, '生意参谋',
                    #                  '2018-08-12', '2018-09-10')
                    # print(new_url)


def url_reader(url):
    rep = requests.get("https://" + url,
                       headers={
                           'Connection': 'keep-alive',
                           'Cache-Control': 'max-age=0',
                           'Accept': '/',
                           'Upgrade-Insecure-Requests': '1',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'cookie': 'cookie2=116001fb5ac62f2f18afc90e45948273'
                       }
                       )
    return rep.content.decode()


if __name__ == '__main__':
    main()

# print(rep)
# 5801
