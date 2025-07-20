# app/services/dashboard_service.py

from app.models.db import Reservation, User
from app.extensions import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

class DashboardService:

    @staticmethod
    def get_reservations_last_7_days():
        today = datetime.today().date()
        start_date = today - timedelta(days=6)

        daily_data = db.session.query(
            Reservation.reservation_date,
            func.count(Reservation.id)
        ).filter(
            Reservation.reservation_date >= start_date,
            Reservation.reservation_date <= today
        ).group_by(
            Reservation.reservation_date
        ).order_by(Reservation.reservation_date).all()

        date_range = [start_date + timedelta(days=i) for i in range(7)]
        date_dict = {date: count for date, count in daily_data}
        return [(date, date_dict.get(date, 0)) for date in date_range]

    @staticmethod
    def get_top_users(limit=5):
        return db.session.query(
            User.username,
            func.count(Reservation.id).label('reservation_count')
        ).join(
            Reservation, User.id == Reservation.customer_id
        ).group_by(
            User.username
        ).order_by(
            desc('reservation_count')
        ).limit(limit).all()

    @staticmethod
    def get_recent_reservations(limit=5):
        reservations = (
            db.session.query(Reservation)
            .options(db.joinedload(Reservation.customer))
            .order_by(desc(Reservation.created_at))
            .limit(limit)
            .all()
        )

        resultado = []
        for r in reservations:
            username = r.customer.username if r.customer else '—'
            resultado.append({
                'id': r.id,
                'reservation_date': r.reservation_date.strftime('%Y-%m-%d'),
                'reservation_time': r.reservation_time.strftime('%H:%M'),
                'username': username
            })
        return resultado

    @staticmethod
    def get_recent_users(limit=5):
        users = (
            db.session.query(User)
            .order_by(desc(User.created_at))
            .limit(limit)
            .all()
        )
        resultado = []
        for u in users:
            created = u.created_at.strftime('%Y-%m-%d %H:%M') if u.created_at else '—'
            resultado.append({
                'username': u.username,
                'created_at': created
            })
        return resultado
