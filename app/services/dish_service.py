from app.extensions import db
from app.models.db import Dish
from app.factories.dish_factory import DishFactory
from app.dtos.dish_dto import DishDTO

class DishService:
    factory = DishFactory()  # Usamos una instancia, no métodos estáticos

    @staticmethod
    def get_by_restaurant(restaurant):
        return [DishService.factory.create_dto_from_model(d) for d in restaurant.dishes]

    @staticmethod
    def get_by_id(dish_id):
        dish = Dish.query.get(dish_id)
        return DishService.factory.create_dto_from_model(dish) if dish else None

    @staticmethod
    def create(dto: DishDTO) -> bool:
        try:
            dish = DishService.factory.create_model_from_dto(dto)
            db.session.add(dish)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el plato: {e}")
            return False

    @staticmethod
    def update(dish_id, dto: DishDTO) -> bool:
        dish = Dish.query.get(dish_id)
        if not dish:
            return False
        dish.name = dto.name
        dish.ingredients = dto.ingredients
        dish.description = dto.description
        dish.price = dto.price
        dish.image_filename = dto.image_filename
        db.session.commit()
        return True

    @staticmethod
    def delete(dish_id) -> bool:
        dish = Dish.query.get(dish_id)
        if dish:
            db.session.delete(dish)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_by_restaurant_id(restaurant_id):
        return Dish.query.filter_by(restaurant_id=restaurant_id).all()

