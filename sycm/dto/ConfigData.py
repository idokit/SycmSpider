from sycm.entity.UserParams import UserParams
from sycm.entity.SycmCategory import SycmCategory
from sycm.entity.TaskProgress import TaskProgress
from sycm.exception.fieldDontMatchException import FieldDontMatchException
from sycm.customEnums.formEnum import ShopType, DateType, DeviceType
from .Dto import Dto
import logging
import json
import datetime

dataConfig_logger = logging.getLogger("数据库配置")


# from customEnum.formEnum import DateType

class ConfigData(object):
    __sql_address__ = "mysql+mysqlconnector://py_sycm:Kdi*33lSI@120.55.113.9:3306/toothpick"

    __name_lit__ = ('美容护肤/美体/精油', '彩妆/香水/美妆工具')

    def __init__(self):
        pass

    def updateDate_where_data_type(self, data_type, time_dimension, current_date):
        session = Dto(self.__sql_address__)
        try:
            session.query(TaskProgress).filter(
                TaskProgress.data_type == data_type, TaskProgress.time_dimension == time_dimension).update(
                {
                    # TaskProgress.next_time: current_date
                    TaskProgress.next_time: datetime.datetime.strptime(current_date, "%Y-%m-%d")
                }
            )
            session.commit()
        except Exception as e:
            dataConfig_logger.error("进度更新失败：类型： %s 时间维度 %s 日期进度：%s" % (
                data_type, time_dimension, current_date) + str(e))
        finally:
            session.close()

    # 获取任务进度日期的方法
    def get_current_date_where_data_type_and_time_dimension(self, data_type, time_dimension):
        session = Dto(self.__sql_address__)
        task_progress = None
        try:
            task_progress = session.query(TaskProgress).filter(
                TaskProgress.data_type == data_type, TaskProgress.time_dimension == time_dimension).one()
        except Exception as e:
            dataConfig_logger.error('数据库未查询到%s and %s' %
                                    (data_type, time_dimension) + str(e))
        return task_progress

    def new_band_config(self):
        return self.newFindByName('商品店铺榜-品牌粒度')

    def new_product_config(self):
        return self.newFindByName('商品店铺榜-产品粒度')

    def newFindByName(self, data_type):
        session = Dto(self.__sql_address__)
        conf_list = session.query(UserParams).filter(
            UserParams.data_type == data_type).all()
        chain_list = list()
        for conf in conf_list:
            conf_detail = json.loads(conf.value)
            conf_details = conf_detail['userParams']['品牌类目列表']
            for cate in conf_details:
                # cate_chain = list()
                cate_chain = dict()
                itemName = cate['一级类目']
                try:
                    category_detail = session.query(SycmCategory).filter(
                        SycmCategory.level == 1, SycmCategory.name == itemName).one()
                except Exception as e:
                    dataConfig_logger.error("通过类目名%s获取id失败%s" % (
                        itemName, category_detail.id) + str(e))

                if data_type == '商品店铺榜-品牌粒度':
                    cate_chain = {
                        'itemName': itemName,
                        'cateId': category_detail.id,
                        'bandName': cate['品牌名'],
                        'bandCount': cate['品牌序号'],
                        'shopName': conf.shop
                    }
                if data_type == '商品店铺榜-产品粒度':
                    cate_chain = {
                        'itemName': itemName,
                        'cateId': category_detail.id,
                        'bandName': cate['品牌名'],
                        'bandCount': cate['品牌序号'],
                        'productName': cate['产品名'],
                        'productCount': cate['产品序号'],
                        'shopName': conf.shop
                    }
                cate_chain['depth'] = 1
                if cate['二级类目'] != "":
                    itemName = cate['二级类目']
                    try:
                        category_detail = session.query(SycmCategory).filter(
                            SycmCategory.level == 2, SycmCategory.name == itemName,
                            SycmCategory.parent_id == cate_chain['cateId']).one()
                        if data_type == '商品店铺榜-品牌粒度':
                            cate_chain['subcate'] = {
                                'itemName': itemName,
                                'cateId': category_detail.id,
                                'bandName': cate['品牌名'],
                                'bandCount': cate['品牌序号'],
                                'shopName': conf.shop
                            }
                        if data_type == '商品店铺榜-产品粒度':
                            cate_chain['subcate'] = {
                                'itemName': itemName,
                                'cateId': category_detail.id,
                                'bandName': cate['品牌名'],
                                'bandCount': cate['品牌序号'],
                                'productName': cate['产品名'],
                                'productCount': cate['品牌序号'],
                                'shopName': conf.shop
                            }
                    except Exception as e:
                        dataConfig_logger.error("通过品牌名%s获取id失败%s" % (
                            itemName, category_detail.id) + str(e))
                    cate_chain['depth'] = 2
                if cate['三级类目'] != "":
                    itemName = cate['三级类目']
                    try:
                        category_detail = session.query(SycmCategory).filter(
                            SycmCategory.level == 3, SycmCategory.name == itemName,
                            SycmCategory.parent_id == cate_chain['subcate']['cateId']).one()
                        if data_type == '商品店铺榜-品牌粒度':
                            cate_chain['subcate']['subcate'] = {
                                'itemName': itemName,
                                'cateId': category_detail.id,
                                'bandName': cate['品牌名'],
                                'bandCount': cate['品牌序号'],
                                'shopName': conf.shop
                            }
                        if data_type == '商品店铺榜-产品粒度':
                            cate_chain['subcate']['subcate'] = {
                                'itemName': itemName,
                                'cateId': category_detail.id,
                                'bandName': cate['品牌名'],
                                'bandCount': cate['品牌序号'],
                                'productName': cate['产品名'],
                                'productCount': cate['品牌序号'],
                                'shopName': conf.shop
                            }
                    except Exception as e:
                        dataConfig_logger.error("通过品牌名%s获取id失败%s" % (
                            itemName, category_detail.id) + str(e))
                    cate_chain['depth'] = 3
                chain_list.append(cate_chain)
                session.close()
        return chain_list

    def getFullCate(self, needJunjor=True, seniorName=('美容护肤/美体/精油', '彩妆/香水/美妆工具')):
        session = Dto(self.__sql_address__)

        conf_list = session.query(SycmCategory).filter(
            SycmCategory.name.in_(seniorName)
        )
        chain = list()
        for cate in conf_list:
            chain.append({
                'itemName': cate.name,
                'cateId': cate.id,
                'depth': 1
            })
            subcates = session.query(SycmCategory).filter(SycmCategory.parent_id == cate.id)
            for subcate in subcates:
                chain.append(
                    {
                        'itemName': cate.name,
                        'cateId': cate.id,
                        'depth': 2,
                        'subcate': {
                            'itemName': subcate.name,
                            'cateId': subcate.id
                        }
                    }
                )
                if needJunjor:
                    juniorCates = session.query(SycmCategory).filter(SycmCategory.parent_id == subcate.id).all()
                    if len(juniorCates) != 0:
                        for juniorCate in juniorCates:
                            chain.append(
                                {
                                    'itemName': cate.name,
                                    'cateId': cate.id,
                                    'depth': 3,
                                    'subcate': {
                                        'itemName': subcate.name,
                                        'cateId': subcate.id,
                                        'subcate': {
                                            'itemName': juniorCate.name,
                                            'cateId': juniorCate.id,
                                        }
                                    }
                                }
                            )
        return chain

    # 获取搜索词
    def get_searchwords(self, data_type):
        session = Dto(self.__sql_address__)
        conf = session.query(UserParams).filter(UserParams.data_type == data_type).one()
        temp = json.loads(conf.value)
        searchwords_list = temp['userParams']['搜索词列表']
        session.close()
        return searchwords_list

    @staticmethod
    def tb_concat(tb, common_tb):
        for val in tb:
            val = val + common_tb
            yield val

    @staticmethod
    def getCateId(selection):
        if not selection['depth']:
            dataConfig_logger.error("获取depth字段失败" + str(selection))
            return
        if selection['depth'] == 1:
            return selection['cateId']
        elif selection['depth'] == 2:
            return selection['subcate']['cateId']
        elif selection['depth'] == 3:
            return selection['subcate']['subcate']['cateId']
        else:
            return None

    @staticmethod
    def cateField(*, cate, crawl_date, dateType, devcice, seller, **kwarg):
        cate_filed_tr = []
        cate_filed_tb = []
        data_key = []
        if not cate['itemName']:
            dataConfig_logger.error("获取字段名失败" + str(cate))
            return None
        cate_filed_tr.append('一级类目')
        data_key.append(DateType[dateType].value)
        data_key.append(cate['itemName'])
        cate_filed_tb.append(cate['itemName'])
        if cate['depth'] > 1:
            cate_filed_tr.append('二级类目')
            cate_filed_tb.append(cate['subcate']['itemName'])
            data_key.append(cate['subcate']['itemName'])
        if cate['depth'] > 2:
            cate_filed_tr.append('三级类目')
            cate_filed_tb.append(cate['subcate']['subcate']['itemName'])
            data_key.append(cate['subcate']['subcate']['itemName'])
        cate_filed_tr.append('类目层级')
        if cate['depth'] == 1:
            cate_filed_tb.append('一级')
        if cate['depth'] == 2:
            cate_filed_tb.append('二级')
        if cate['depth'] == 3:
            cate_filed_tb.append('三级')
        cate_filed_tr.append('日期')
        cate_filed_tr.append('周期')
        cate_filed_tr.append('终端')
        cate_filed_tr.append('店铺类型')
        if dateType == 'day' or 'recent1':
            cate_filed_tb.append(str(crawl_date))
        elif dateType == 'month' or 'range':
            cate_filed_tb.append(str(crawl_date[0]))
        cate_filed_tb.append(DateType[dateType].value)
        cate_filed_tb.append(DeviceType.getNameFromValue(devcice))
        cate_filed_tb.append(ShopType.getNameFromValue(seller))
        data_key.append(DeviceType.getNameFromValue(devcice))
        data_key.append(ShopType.getNameFromValue(seller))

        if len(cate_filed_tr) != len(cate_filed_tb):
            raise FieldDontMatchException(cate_filed_tr, cate_filed_tb)
        return cate_filed_tr, cate_filed_tb, data_key
