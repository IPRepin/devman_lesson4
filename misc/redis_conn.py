import redis

from config import (REDIS_HOST, REDIS_PORT, REDIS_DB)


def get_redis_conn():
    redis_connect = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    return redis_connect
