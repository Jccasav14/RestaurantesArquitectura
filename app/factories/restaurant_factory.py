from app.models.db import Restaurant
from app.dtos.restaurant_dto import RestaurantDTO
from app.factories.base_factory import AbstractFactory

class RestaurantFactory(AbstractFactory):

    def create_dto_from_model(self, restaurant: Restaurant) -> RestaurantDTO:
        return RestaurantDTO(
            id=restaurant.id,
            name=restaurant.name,
            address=restaurant.address,
            phone=restaurant.phone,
            description=restaurant.description,
            image_filename=restaurant.image_filename
        )

    def create_model_from_dto(self, dto: RestaurantDTO) -> Restaurant:
        return Restaurant(
            id=dto.id,
            name=dto.name,
            address=dto.address,
            phone=dto.phone,
            description=dto.description,
            image_filename=dto.image_filename
        )
