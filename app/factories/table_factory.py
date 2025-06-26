from app.models.db import Table
from app.dtos.table_dto import TableDTO

class TableFactory:
    @staticmethod
    def create_dto_from_model(table: Table) -> TableDTO:
        return TableDTO(
            id=table.id,
            number=table.number,
            type=table.type,
            capacity=table.capacity,
            description=table.description,
            restaurant_id=table.restaurant_id
        )

    @staticmethod
    def create_model_from_dto(dto: TableDTO) -> Table:
        return Table(
            number=dto.number,
            type=dto.type,
            capacity=dto.capacity,
            description=dto.description,
            restaurant_id=dto.restaurant_id
        )