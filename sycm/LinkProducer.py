# 生成要爬取的链接
import datetime
import re

from sycm.dto.ConfigData import ConfigData
from sycm.lib.RedisClient import RedisClient
import pandas as pd


def main():
    start_time = '2018-09-05'
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    start_time = datetime.date(*[int(i) for i in start_time.split('-')])
    db = RedisClient('127.0.0.1', '6379')
    cates = ConfigData().getFullCate()
    for dateType in ['day', 'week', 'month']:
        crawl_dates = []
        if dateType == 'day':
            crawl_dates = [[i.strftime('%Y-%m-%d'), i.strftime('%Y-%m-%d')] for i in
                           pd.date_range(start_time, yesterday).date]
        elif dateType == 'week':
            # 判断开始时间是不是星期一
            current_week = start_time.isoweekday()
            if current_week != 1:
                monday = start_time + datetime.timedelta(
                    days=7 - current_week)
                # 如果当前这个星期一距离现在不足7天
                crawl_dates = [[i.strftime('%Y-%m-%d'), (i + datetime.timedelta(days=6)).strftime('%Y-%m-%d')] for i
                               in pd.date_range(monday, yesterday, freq='7D').date if (yesterday - i).days > 7]
            else:
                crawl_dates = [[i.strftime('%Y-%m-%d'), (i + datetime.timedelta(days=6)).strftime('%Y-%m-%d')] for i
                               in pd.date_range(start_time, yesterday, freq='7D').date if (yesterday - i).days > 7]
        elif dateType == 'month':
            crawl_dates = [[datetime.date(v.year, v.month, 1).strftime('%Y-%m-%d'), v.strftime('%Y-%m-%d')] for v in
                           pd.date_range(start_time, yesterday, freq='1M').date]
        for crawl_date in crawl_dates:
            for device in [0, 2]:
                for cate in cates:
                    for seller in [-1, 1]:
                        url = "https://sycm.taobao.com/mc/mq/overview?cateFlag=0&cateId={}&dateRange={}&dateType={}&device={}&sellerType={}".format(
                            cate, crawl_date[0] + "%7c" + crawl_date[1], dateType, device, seller)
                        db.add('compeletion:start_urls', url)
                        print(url)


if __name__ == '__main__':
    main()
