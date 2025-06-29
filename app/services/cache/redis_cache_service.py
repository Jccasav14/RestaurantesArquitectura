import redis
import json
from .cache_service_interface import ICacheService

#Implementación concreta del servicio de cache usando Redis
class RedisCacheService(ICacheService):
    #Constructor de la clase, establece la conexión con el servidor Redis
    def __init__(self, host='redis', port=6379, db=0):
        # Crea una instancia de cliente Redis
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    #Recupera un valor del cache a partir de su clave
    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None # Convierte el JSON almacenado de vuelta a objeto Python

    # Guarda un valor en el cache, con tiempo de expiración
    def set(self, key, value, ex=300):
        self.redis.set(key, json.dumps(value), ex=ex)   # Se almacena en Redis como JSON string

    #Elimina un valor del cache
    def delete(self, key):
        self.redis.delete(key)
