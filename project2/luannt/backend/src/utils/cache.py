from redis import Redis
from bson import json_util

redis_client = Redis(host='redis', port=6379, db=0)
# redis_client = Redis(host='localhost', port=6379, db=0)

def cache_data(redis_client, cache_key, data):
    redis_client.set(cache_key, json_util.dumps(data))
