# app/__init__.py
from flask import Flask, redirect, url_for  # <-- AÑADIDO
from app.extensions import db, login_manager
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.db import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importación y registro de Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.customer_controller import customer_bp         
    from app.controllers.restaurant_controller import restaurant_bp
    from app.controllers.dish_controller import dish_bp
    from app.controllers.table_controller import table_bp
    from app.controllers.reservation_controller import reservation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(dish_bp)
    app.register_blueprint(table_bp)
    app.register_blueprint(reservation_bp)

    # ✅ Ruta raíz que redirige al login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
