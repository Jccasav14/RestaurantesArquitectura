from app.models.db import Category, db
from app.dtos.category_dto import CategoryDTO
from app.factories.category_factory import CategoryFactory

class CategoryService:
    @staticmethod
    def get_all():
        return [CategoryFactory.model_to_dto(c) for c in Category.query.all()]

    @staticmethod
    def get_by_id(category_id):
        category = Category.query.get(category_id)
        return CategoryFactory.model_to_dto(category) if category else None

    @staticmethod
    def create(dto: CategoryDTO):
        category = CategoryFactory.dto_to_model(dto)
        db.session.add(category)
        db.session.commit()
        return True

    @staticmethod
    def update(category_id, dto: CategoryDTO):
        category = Category.query.get(category_id)
        if not category:
            return False
        category.name = dto.name
        db.session.commit()
        return True

    @staticmethod
    def delete(category_id):
        category = Category.query.get(category_id)
        if not category:
            return False
        db.session.delete(category)
        db.session.commit()
        return True
