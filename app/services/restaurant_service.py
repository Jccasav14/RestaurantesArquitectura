from app.models.db import Restaurant
from app.extensions import db
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.restaurant_factory import RestaurantFactory

class RestaurantService:
    factory = RestaurantFactory()

    @staticmethod
    def get_all():
        restaurants = Restaurant.query.all()
        return [RestaurantService.factory.create_dto_from_model(r) for r in restaurants]

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
