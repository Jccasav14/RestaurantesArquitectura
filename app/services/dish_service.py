from app.extensions import db
from app.models.db import Dish
from app.factories.dish_factory import DishFactory
from app.dtos.dish_dto import DishDTO

class DishService:
    # Se instancia una fábrica para conversión entre modelos y DTOs
    factory = DishFactory()

    #Devuelve todos los platos de un restaurante específico
    @staticmethod
    def get_by_restaurant(restaurant):
        return [DishService.factory.create_dto_from_model(d) for d in restaurant.dishes]

    # Busca un plato por su ID
    @staticmethod
    def get_by_id(dish_id):
        dish = Dish.query.get(dish_id)
        return DishService.factory.create_dto_from_model(dish) if dish else None

    #Crea un nuevo plato en la base de datos a partir de un DTO
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

    #Actualiza los datos de un plato existente
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

    #Elimina un plato por ID
    @staticmethod
    def delete(dish_id) -> bool:
        dish = Dish.query.get(dish_id)
        if dish:
            db.session.delete(dish)
            db.session.commit()
            return True
        return False
    
    #Devuelve todos los platos pertenecientes a un restaurante por su ID
    @staticmethod
    def get_by_restaurant_id(restaurant_id):
        return Dish.query.filter_by(restaurant_id=restaurant_id).all()

