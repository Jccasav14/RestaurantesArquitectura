from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db  
from datetime import datetime



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'admin' o 'customer'

    # Métodos requeridos por Flask-Login
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    # Métodos para contraseñas
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(200))  # ← Aquí se guarda el nombre de la imagen
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='restaurants')
    tables = db.relationship('Table', back_populates='restaurant', cascade='all, delete-orphan')
    

class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(200))

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref='dishes')

class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Ej: 'vip', 'normal'
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    restaurant = db.relationship('Restaurant', back_populates='tables')

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.Time, nullable=False)
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    menu = db.Column(db.String(255), nullable=True)


    # Relaciones
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer = db.relationship('User', backref='reservations', lazy=True)
    restaurant = db.relationship('Restaurant', backref='reservations', lazy=True)
    table = db.relationship('Table', backref='reservations', lazy=True)