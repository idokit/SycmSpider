from enum import Enum


class ShopType(Enum):
    # 店铺分类
    quanwang = (-1, "全网")
    taobao = (-1, "淘宝")
    tianmao = (1, "天猫")

    @classmethod
    def getNameFromValue(cls, val):
        for member in cls:
            if member.value[0] == val:
                return member.value[1]


class DateType(Enum):
    day = "天"
    month = "月"
    range = "自定义"
    recent1 = "最近一天"


class DeviceType(Enum):
    # 终端分类
    all = (0, "所有终端")
    pc = (1, "PC端")
    wuxian = (1, "无线端")

    @classmethod
    def getNameFromValue(cls, val):
        for member in cls:
            if member.value[0] == val:
                return member.value[1]
