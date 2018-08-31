from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class DataSource(Base):
    __tablename__ = 'data_source'
    id = Column(BigInteger, primary_key=True)
    # '店铺名',
    shop_name = Column(String(128))
    # '数据类型（报表名）',
    data_type = Column(String(128))
    # '数据行索引',
    data_key = Column(String(128))
    # '数据值',
    value = Column(String(5000))
    # 平台名称
    pt_name = Column(String(64))
    # 数据起始时间
    start_time = Column(DateTime())
    # 数据结束时间
    end_time = Column(DateTime())
    # 修改时间
    gmt_create = Column(DateTime())
