from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


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
    # def to_data_base(self,data_type,tb,tr):
    #     for item in data:
    #         for tb_val in item.tb:
    #             spider.db.add(DataSource(**{
    #                 'shop_name': '宝洁',
    #                 'data_type': item.name,
    #                 'data_key': 'data_key',
    #                 'value': json.dumps(dict(zip(map(lambda v: v.text, item.tr), map(lambda v: v.text, tb_val))),
    #                                     ensure_ascii=False),
    #                 'pt_name': '平台名',
    #                 'start_time': crawl_date,
    #                 'end_time': crawl_date + datetime.timedelta(1),
    #                 'gmt_create': datetime.datetime.now()
    #             }))
    #     spider.db.commit()
