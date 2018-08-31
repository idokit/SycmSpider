from sqlalchemy import Column, String, BigInteger, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()


class TaskProgress(Base):
    __tablename__ = 'task_progress'

    id = Column(BigInteger, primary_key=True)
    # 数据类型
    data_type = Column(String(128))
    # '时间维度',
    time_dimension = Column(String(8))
    # 数据起始时间
    next_time = Column(DateTime)
    # 数据结束时间
    gmt_modify = Column(DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)

