from sqlalchemy import Column, String, BigInteger, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class SycmCategory(Base):
    __tablename__ = 'sycm_category'

    id = Column(BigInteger, primary_key=True)
    # '父类Id',
    parent_id = Column(BigInteger)
    # '名称',
    name = Column(String(128))

    level = Column(Integer)
    # 数据起始时间
    gmt_create = Column(DateTime())
    # 数据结束时间
    gmt_modify = Column(DateTime())
    # 修改时间
