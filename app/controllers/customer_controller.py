from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user  # ← esto también

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('customer/dashboard.html', user=current_user)
