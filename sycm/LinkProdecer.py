# 生成要爬取的链接
import datetime
import re

from sycm.dto.ConfigData import ConfigData
from sycm.lib.RedisClient import RedisClient


def main():
    yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")
    for dateType in ['day']:
        crawl_date = [[yesterday, yesterday]]
        for crawl_date in crawl_date:
            for device in [0, 2]:
                cates = ConfigData().getFullCate()
                for cate in cates:
                    for seller in [-1, 1]:
                        url = "https://sycm.taobao.com/mc/mq/overview?cateFlag=0&cateId={}&dateRange={}&dateType={}&device={}&sellerType={}".format(
                            cate, yesterday + "%7c" + yesterday, dateType, device, seller)
                        db = RedisClient('127.0.0.1','6379')
                        db.add('compeletion:start_urls',url)


if __name__ == '__main__':
    main()