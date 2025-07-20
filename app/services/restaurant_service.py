from app.models.db import Restaurant
from app.extensions import db
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.restaurant_factory import RestaurantFactory
from app.factories.cache_factory import CacheFactory
from app.services.cache.redis_cache_service import RedisCacheService


class RestaurantService:
    # Instancia de la factory que transforma entre Modelos y DTOs
    factory = RestaurantFactory()

    # Instancia del servicio de caché (Redis)
    cache = RedisCacheService()

    #Devuelve la lista de todos los restaurantes
    @staticmethod
    def get_all():
        cache_key = 'restaurant_list'
        cached_data = RestaurantService.cache.get(cache_key)
        if cached_data:
            # Si hay en caché, reconstruimos los DTOs desde los diccionarios almacenados
            return [RestaurantDTO(**r) for r in cached_data]

        # Si no hay en caché, consulta la base de datos
        restaurants = Restaurant.query.all()
        # Convertimos a DTOs, y luego a dict para guardarlo en caché
        dto_list = [RestaurantService.factory.create_dto_from_model(r).to_dict() for r in restaurants]
        # Guardar en cache
        RestaurantService.cache.set(cache_key, dto_list)
        # Retornar los DTOs
        return [RestaurantDTO(**r) for r in dto_list]


    #Obtiene un restaurante por su ID
    @staticmethod
    def get_by_id(restaurant_id):
        cache_key = f'restaurant:{restaurant_id}'
        cached = RestaurantService.cache.get(cache_key)
        if cached:
            return RestaurantDTO(**cached)

        restaurant = Restaurant.query.get(restaurant_id)
        dto = RestaurantService.factory.create_dto_from_model(restaurant).to_dict()
        RestaurantService.cache.set(cache_key, dto)
        return RestaurantDTO(**dto)


    #Elimina un restaurante por su ID
    @staticmethod
    def delete(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            RestaurantService.cache.delete('restaurant_list')
            return True
        return False

    #Crea un nuevo restaurante usando el DTO recibido
    @staticmethod
    def create(dto: RestaurantDTO, created_by: int) -> bool:
        try:
            restaurant = RestaurantService.factory.create_model_from_dto(dto)
            restaurant.created_by = created_by
            db.session.add(restaurant)
            db.session.commit()

            RestaurantService.cache.delete('restaurant_list')

            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear restaurante: {e}")
            return False
    
    #Actualiza un restaurante existente
    @staticmethod
    def update(restaurant_id: int, dto: RestaurantDTO) -> bool:
        try:
            restaurant = Restaurant.query.get(restaurant_id)
            if not restaurant:
                return False

            # Actualiza campos básicos
            restaurant.name = dto.name
            restaurant.address = dto.address
            restaurant.phone = dto.phone
            restaurant.description = dto.description
            restaurant.image_filename = dto.image_filename

            db.session.commit()

            RestaurantService.cache.delete('restaurant_list')

            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar restaurante: {e}")
            return False

