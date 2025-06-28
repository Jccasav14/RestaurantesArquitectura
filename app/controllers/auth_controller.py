from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.models.db import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_after_login()
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect_after_login()
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def redirect_after_login():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('customer.frequent_restaurants'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role') or 'customer'  # Asigna 'customer' por defecto si no se indica

        # Validaciones básicas
        if not username or not email or not password or not confirm_password:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        # Verificar si el usuario o email ya existen
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('El nombre de usuario o el correo ya están registrados.', 'error')
            return render_template('register.html')

        # Crear nuevo usuario
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)  # Usa el método seguro del modelo

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado exitosamente. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al registrar: {str(e)}', 'error')

    return render_template('register.html')


@auth_bp.route('/forgot-password', methods=['GET'])
def forgot_password():
    # Lógica para recuperar contraseña
    return render_template('forgot_password.html')