from app.models.db import Restaurant
from app.extensions import db
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.restaurant_factory import RestaurantFactory
from app.factories.cache_factory import CacheFactory


class RestaurantService:
    factory = RestaurantFactory()

    @staticmethod
    def get_all():
        cache = CacheFactory.get_cache_service()
        cache_key = "restaurants_all"

        cached_data = cache.get(cache_key)
        if cached_data:
            # Reconstruir DTOs desde dicts
            return [RestaurantDTO(**item) for item in cached_data]

        restaurants = Restaurant.query.all()
        dto_list = [RestaurantService.factory.create_dto_from_model(r) for r in restaurants]

        # Convertir a dicts antes de almacenar
        dto_dicts = [dto.to_dict() for dto in dto_list]
        cache.set(cache_key, dto_dicts)

        return dto_list



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
            return True
        return False

    @staticmethod
    def create(dto: RestaurantDTO, created_by: int) -> bool:
        try:
            restaurant = RestaurantService.factory.create_model_from_dto(dto)
            restaurant.created_by = created_by
            db.session.add(restaurant)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear restaurante: {e}")
            return False
