from sqlalchemy import func
from app.models.db import Reservation
from app.extensions import db

class ReservationStatsService:
    #Obtiene estadísticas de reservaciones de un cliente específico, por fechas
    @staticmethod
    def get_reservations_by_date(user_id):
        results = (
            db.session.query(
                func.date(Reservation.reservation_date), # Agrupamos por solo la fecha (sin hora)
                func.count()    # Contamos número de reservaciones por fecha
            )
            .filter(Reservation.customer_id == user_id) # Solo para el cliente indicado
            .group_by(func.date(Reservation.reservation_date))  # Agrupamos por fecha
            .order_by(func.date(Reservation.reservation_date))  # Orden cronológico
            .all()
        )
        # Convertimos el resultado en lista de diccionarios
        return [{"date": str(r[0]), "total": r[1]} for r in results]
