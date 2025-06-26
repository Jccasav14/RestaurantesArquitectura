from app.services.cache.redis_cache_service import RedisCacheService

class CacheFactory:
    @staticmethod
    def get_cache_service():
        return RedisCacheService()
