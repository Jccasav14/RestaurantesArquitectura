from app.models.db import Restaurant
from app.extensions import db
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.restaurant_factory import RestaurantFactory
from app.factories.cache_factory import CacheFactory
from app.services.cache.redis_cache_service import RedisCacheService


class RestaurantService:
    factory = RestaurantFactory()
    cache = RedisCacheService()  # instancia del cache

    @staticmethod
    def get_all():
        cache_key = 'restaurant_list'
        cached_data = RestaurantService.cache.get(cache_key)
        if cached_data:
            return [RestaurantDTO(**r) for r in cached_data]

        restaurants = Restaurant.query.all()
        dto_list = [RestaurantService.factory.create_dto_from_model(r).to_dict() for r in restaurants]
        RestaurantService.cache.set(cache_key, dto_list)
        return [RestaurantDTO(**r) for r in dto_list]



    @staticmethod
    def get_by_id(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        return RestaurantService.factory.create_dto_from_model(restaurant) if restaurant else None

    @staticmethod
    def delete(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            RestaurantService.cache.delete('restaurant_list')
            return True
        return False

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
        
    @staticmethod
    def update(restaurant_id: int, dto: RestaurantDTO) -> bool:
        try:
            restaurant = Restaurant.query.get(restaurant_id)
            if not restaurant:
                return False

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

