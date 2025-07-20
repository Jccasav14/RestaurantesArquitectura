# app/controllers/stats_controller.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import os
import redis

stats_bp = Blueprint('stats', __name__)

# 🔌 Conexión a Redis (el host es el nombre del servicio en docker-compose)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@stats_bp.before_app_request
def log_request():
    if not request.endpoint or request.endpoint.startswith('static'):
        return  # ignorar peticiones estáticas

    instance = os.getenv("HOSTNAME", "unknown")
    r.incr(f"requests:{instance}")
    print(f"[{instance}] {request.method} {request.path}")

@stats_bp.route('/stats')
@login_required
def stats():
    # 👮‍♂️ Solo administradores pueden ver esta página
    if current_user.role != 'admin':
        flash('No tienes permiso para esta sección', 'error')
        return redirect(url_for('auth.login'))

    # 🔢 Obtener todos los contadores de Redis
    keys = r.keys("requests:*")
    stats_data = {key.split(":")[1]: r.get(key) for key in keys}

    return render_template("stats.html", stats=stats_data, user=current_user.username)
