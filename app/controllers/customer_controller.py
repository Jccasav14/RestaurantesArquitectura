from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.user_service import UserService
from app.dtos.user_dto import UserDTO
from app.models.db import User

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('customer/dashboard.html', user=current_user)