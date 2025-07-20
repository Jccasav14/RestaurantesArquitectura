from app.extensions import db
from app.models.db import Table
from app.factories.table_factory import TableFactory
from app.dtos.table_dto import TableDTO

class TableService:

    #Obtiene todas las mesas de un restaurante específico
    @staticmethod
    def get_by_restaurant(restaurant_id):
        tables = Table.query.filter_by(restaurant_id=restaurant_id).all()
        return [TableFactory.create_dto_from_model(t) for t in tables]

    #Obtiene una mesa por su ID
    @staticmethod
    def get_by_id(table_id):
        table = Table.query.get(table_id)
        return TableFactory.create_dto_from_model(table) if table else None

    #Crea una nueva mesa en la base de datos a partir de un DTO
    @staticmethod
    def create(dto: TableDTO) -> bool:
        try:
            # Convertimos el DTO a modelo de base de datos
            table = TableFactory.create_model_from_dto(dto)
            db.session.add(table)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear mesa: {e}")
            return False

    #Actualiza los datos de una mesa existente usando un DTO
    @staticmethod
    def update(table_id, dto: TableDTO) -> bool:
        table = Table.query.get(table_id)
        if not table:
            return False
        # Actualizar campos
        table.number = dto.number
        table.type = dto.type
        table.capacity = dto.capacity
        table.description = dto.description
        db.session.commit()
        return True

    #Elimina una mesa por su ID
    @staticmethod
    def delete(table_id) -> bool:
        table = Table.query.get(table_id)
        if table:
            db.session.delete(table)
            db.session.commit()
            return True
        return False

    #Retorna todas las mesas de un restaurante específico
    @staticmethod
    def get_by_restaurant_id(restaurant_id):
        return Table.query.filter_by(restaurant_id=restaurant_id).all()
