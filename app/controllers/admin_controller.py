from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.db import User



admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html', user=current_user)

@admin_bp.route('/usuarios')
@login_required
def list_users():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    
    users = User.query.filter_by(role='customer').all()
    return render_template('admin/user_list.html', users=users)

