import redis

from sycm.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, key, val):
        self.db.lpush(key, val)

    def exists(self, key, val):
        return not self.db.lindex(key, val)

    def count(self, key):
        return self.db.llen(key)

    def delete(self, key, val):
        return self.db.lpushx(key, val)
