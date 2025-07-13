from app.models.db import Category
from app.dtos.category_dto import CategoryDTO

class CategoryFactory:
    @staticmethod
    def model_to_dto(model: Category) -> CategoryDTO:
        return CategoryDTO(
            id=model.id,
            name=model.name
        )

    @staticmethod
    def dto_to_model(dto: CategoryDTO) -> Category:
        return Category(name=dto.name)
