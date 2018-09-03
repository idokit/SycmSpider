import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sycm.entity.DataSource import DataSource


class Dto():
    def __init__(self, sql_address):
        engine = create_engine(sql_address)
        self._session = sessionmaker(bind=engine)()

    def add(self, entity):
        return self._session.add(entity)

    def commit(self):
        return self._session.commit()

    def close(self):
        return self._session.close_all()

    def query(self, *args, **kw):
        return self._session.query(*args, **kw)

    def data_process(self, shop_name, data_type, data_key, value, pt_name, start_time, end_time):
        self.add(
            DataSource(**{
                'shop_name': shop_name,
                'data_type': data_type,
                'data_key': data_key,
                'value': value,
                'pt_name': pt_name,
                'start_time': datetime.datetime.strptime(start_time, "%Y-%m-%d"),
                'end_time': datetime.datetime.strptime(end_time, "%Y-%m-%d"),
                'gmt_create': datetime.datetime.now()
            })
        )
        self.commit()