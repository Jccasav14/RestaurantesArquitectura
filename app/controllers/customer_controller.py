from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.user_service import UserService
from app.dtos.user_dto import UserDTO
from app.models.db import User
from app.services.restaurant_visit_service import RestaurantVisitService
from app.dtos.restaurant_frequency_dto import RestaurantFrequencyDTO
from app.services.reservation_stats_service import ReservationStatsService 
from app.services.reservation_service import ReservationService

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('customer/dashboard.html', user=current_user)


@customer_bp.route('/frequent-restaurants')
@login_required
def frequent_restaurants():
    if current_user.role != 'customer':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.login'))

    stats = RestaurantVisitService.get_visit_stats(current_user.id)
    dto_list = [RestaurantFrequencyDTO(name or "", count or 0) for name, count in stats.items()]

    reservation_stats = ReservationStatsService.get_reservations_by_date(current_user.id)

    return render_template(
        "customer/frequent_restaurants.html",
        stats=dto_list,
        reservation_stats=reservation_stats
    )