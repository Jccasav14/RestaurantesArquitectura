from app.models.db import Reservation
from app.extensions import db
from app.factories.reservation_factory import ReservationFactory

class ReservationService:
    @staticmethod
    def create(dto):
        try:
            factory = ReservationFactory()
            reservation = factory.create_model_from_dto(dto)  # ✅ Correcto

            db.session.add(reservation)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear reserva: {e}")  # Aquí imprime el error real
            return False


    @staticmethod
    def get_by_id(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        return ReservationFactory.create_dto_from_model(reservation) if reservation else None

    @staticmethod
    def delete(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_all():
        reservations = Reservation.query.all()
        # Si usas Factory, convierte a DTOs
        return [ReservationFactory().create_dto_from_model(r) for r in reservations]
    
    @staticmethod
    def get_by_customer_id(customer_id):
        return Reservation.query.filter_by(customer_id=customer_id).all()
    
    @staticmethod
    def get_reservation_stats_by_day(user_id):
        from app.models.db import Reservation
        from sqlalchemy import func
        result = db.session.query(
            func.date(Reservation.date_time),
            func.count(Reservation.id)
        ).filter_by(user_id=user_id).group_by(func.date(Reservation.date_time)).all()

        return [{"date": str(r[0]), "total": r[1]} for r in result]

    
    