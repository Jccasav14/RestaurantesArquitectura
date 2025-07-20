from app.services.cache.redis_cache_service import RedisCacheService

class CacheFactory:

    # Devuelve una instancia del servicio de caché (Redis)
    @staticmethod
    def get_cache_service():
        return RedisCacheService()
