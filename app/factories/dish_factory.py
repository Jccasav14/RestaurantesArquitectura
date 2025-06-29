from app.models.db import Dish
from app.dtos.dish_dto import DishDTO
from app.factories.base_factory import AbstractFactory  

class DishFactory(AbstractFactory): 

    # Convierte un objeto Dish (modelo BD) a DishDTO
    def create_dto_from_model(self, dish: Dish) -> DishDTO:
        return DishDTO(
            id=dish.id,
            name=dish.name,
            ingredients=dish.ingredients,
            description=dish.description,
            price=dish.price,
            image_filename=dish.image_filename,
            restaurant_id=dish.restaurant_id
        )

    # Convierte un DishDTO a un objeto Dish (modelo BD)
    def create_model_from_dto(self, dto: DishDTO) -> Dish:
        return Dish(
            name=dto.name,
            ingredients=dto.ingredients,
            description=dto.description,
            price=dto.price,
            image_filename=dto.image_filename,
            restaurant_id=dto.restaurant_id
        )
