# app/controllers/dashboard_controller.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.dashboard_service import DashboardService
from datetime import datetime

# Blueprint del dashboard admin
dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Verificación de rol de admin
    if current_user.role != 'admin':
        flash("Acceso denegado. Solo administradores pueden ver el dashboard.", "error")
        return redirect(url_for('auth.login'))

    # DEBUG: inicio de la petición al dashboard
    print("▶ Entrando a admin/dashboard")

    # Datos de reservas últimos 7 días
    last7 = DashboardService.get_reservations_last_7_days()
    days = [d.strftime('%Y-%m-%d') for d, _ in last7]
    day_counts = [c for _, c in last7]

    # Datos de top usuarios
    top_users = DashboardService.get_top_users(limit=5)
    user_labels = [u for u, _ in top_users]
    user_counts = [c for _, c in top_users]

    # DEBUG: imprimir datos de gráficos
    print(f"▶ Gráfico reservas días: {days} -> {day_counts}")
    print(f"▶ Gráfico top usuarios: {user_labels} -> {user_counts}")

    # Listas de actividad reciente
    recent_reservations = DashboardService.get_recent_reservations() or []
    recent_users = DashboardService.get_recent_users() or []

    # DEBUG: imprimir listas recientes
    print(f"▶ recent_reservations ({len(recent_reservations)}):", recent_reservations)
    print(f"▶ recent_users ({len(recent_users)}):", recent_users)

    # Renderizar plantilla con todas las variables necesarias
    return render_template(
        'admin/dashboard.html',
        days=days,
        day_counts=day_counts,
        user_labels=user_labels,
        user_counts=user_counts,
        recent_reservations=recent_reservations,
        recent_users=recent_users
    )
