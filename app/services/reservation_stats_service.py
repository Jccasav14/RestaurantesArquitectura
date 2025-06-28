from sqlalchemy import func
from app.models.db import Reservation
from app.extensions import db

class ReservationStatsService:
    @staticmethod
    def get_reservations_by_date(user_id):
        results = (
            db.session.query(
                func.date(Reservation.reservation_date),  # <-- nombre correcto
                func.count()
            )
            .filter(Reservation.customer_id == user_id)
            .group_by(func.date(Reservation.reservation_date))
            .order_by(func.date(Reservation.reservation_date))
            .all()
        )
        return [{"date": str(r[0]), "total": r[1]} for r in results]
