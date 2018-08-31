from sqlalchemy import Column, String, BigInteger, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UserParams(Base):
    __tablename__ = 'user_params'
    id = Column(BigInteger, primary_key=True)
    # '店铺名',
    shop = Column(String(64))
    # '数据类型（报表名）',
    data_type = Column(String(512))
    # '数据值',
    value = Column(Text())
    # 数据起始时间
    gmt_create = Column(DateTime())
    # 数据结束时间
    gmt_modify = Column(DateTime())
    # 修改时间


