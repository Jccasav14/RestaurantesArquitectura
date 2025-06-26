from app.factories.base_factory import AbstractFactory
from app.models.db import User
from app.dtos.user_dto import UserDTO

class UserFactory(AbstractFactory):
    def create_dto_from_model(self, model: User) -> UserDTO:
        return UserDTO(
            id=model.id,
            username=model.username,
            email=model.email,
            role=model.role
        )

    def create_model_from_dto(self, dto: UserDTO) -> User:
        user = User(
            username=dto.username,
            email=dto.email,
            role=dto.role
        )
        if hasattr(dto, 'id') and dto.id:
            user.id = dto.id
        return user
