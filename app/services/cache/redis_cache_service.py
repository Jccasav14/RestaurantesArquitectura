import redis
import json
from .cache_service_interface import ICacheService

class RedisCacheService(ICacheService):
    def __init__(self, host='redis', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key, value, ex=300):
        self.redis.set(key, json.dumps(value), ex=ex)

    def delete(self, key):
        self.redis.delete(key)
