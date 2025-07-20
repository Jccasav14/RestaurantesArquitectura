from app.models.db import Reservation
from app.dtos.reservation_dto import ReservationDTO
from app.factories.base_factory import AbstractFactory

class ReservationFactory(AbstractFactory):

    # Convierte un objeto Reservation (modelo BD) a ReservationDTO
    def create_dto_from_model(self, model: Reservation) -> ReservationDTO:
        return ReservationDTO(
            id=model.id,
            customer_id=model.customer_id,
            restaurant_id=model.restaurant_id,
            table_id=model.table_id,
            reservation_date=model.reservation_date,
            reservation_time=model.reservation_time,
            special_requests=model.special_requests,
            menu=model.menu,
            customer=model.customer,
            restaurant=model.restaurant,
            table=model.table
        )

    # Convierte un ReservationDTO a un objeto Reservation (modelo BD)
    def create_model_from_dto(self, dto: ReservationDTO) -> Reservation:
        return Reservation(
            customer_id=dto.customer_id,
            restaurant_id=dto.restaurant_id,
            table_id=dto.table_id,
            reservation_date=dto.reservation_date,
            reservation_time=dto.reservation_time,
            special_requests=dto.special_requests,
            menu=dto.menu
        )
