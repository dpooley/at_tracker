import json
import redis
import asyncio

from at_tracker.common import config

redis_pool = redis.ConnectionPool(host=config.REDIS_HOST,
                                  port=config.REDIS_PORT,
                                  db=config.REDIS_DB_API,
                                  password=config.REDIS_PASS)

def clean_dict(d):
    if not isinstance(d, dict):
        return d
    return dict((k, clean_dict(v)) for k, v in d.items() if v is not None)

def cache_json_set(key, data):
    d = json.dumps(clean_dict(data))
    return cache_exec('set', key, d)

def cache_json_get(key):
    d = cache_exec('get', key)
    return json.loads(d)

def cache_exec(*args):
    r = redis.Redis(connection_pool=redis_pool)
    response = r.execute_command(*args)
    return response
