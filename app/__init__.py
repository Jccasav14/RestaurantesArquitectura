# app/__init__.py
from flask import Flask
from app.extensions import db, login_manager  # ✅ Importación correcta

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'


    db.init_app(app)  # ✅ Ya está definido arriba, así no falla
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.db import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.customer_controller import customer_bp
    from app.controllers.restaurant_controller import restaurant_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(restaurant_bp)

    return app
