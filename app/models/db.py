from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db  
from datetime import datetime


# Modelo de usuario (admin o cliente)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text)  # Cambiado a Text para hashes largos
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    # Métodos requeridos por Flask-Login
    def is_active(self):
        return True # El usuario siempre está activo

    def get_id(self):
        return str(self.id) # Devuelve el ID como string para el login

    # Métodos para contraseñas
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)   # Guarda la contraseña encriptada

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    # Verifica la contraseña

# Modelo de restaurante
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)    # Nombre del restaurante
    address = db.Column(db.String(200))                 # Dirección
    phone = db.Column(db.String(20))                    # Teléfono
    description = db.Column(db.Text)                    # Descripción
    image_filename = db.Column(db.String(200))          # Nombre del archivo de imagen
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))   # Usuario que lo creó (admin)

    user = db.relationship('User', backref='restaurants')   # Relación: un usuario tiene varios restaurantes
    tables = db.relationship('Table', back_populates='restaurant', cascade='all, delete-orphan')   # Mesas del restaurante
    
# Modelo de plato (Dish)
class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)    # Nombre del plato
    ingredients = db.Column(db.Text, nullable=False)    # Ingredientes
    description = db.Column(db.Text)                    # Descripción opcional
    price = db.Column(db.Float, nullable=False)         # Precio
    image_filename = db.Column(db.String(200))          # Imagen del plato
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id')) #Categoria del plato


    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)  # Restaurante al que pertenece
    restaurant = db.relationship('Restaurant', backref='dishes')    # Relación: un restaurante tiene varios platos

# Modelo de mesa (Table)
class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)      # Número de la mesa
    type = db.Column(db.String(50), nullable=False)     # Tipo (ej: VIP, normal)
    capacity = db.Column(db.Integer, nullable=False)    # Capacidad de personas
    description = db.Column(db.String(255))             # Descripción
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) # Restaurante dueño de la mesa

    restaurant = db.relationship('Restaurant', back_populates='tables')     # Relación inversa con Restaurante

# Tabla intermedia
reservation_dishes = db.Table('reservation_dishes',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservations.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
)

# Modelo Reservation
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

    customer = db.relationship('User', backref='reservations', lazy=True)
    restaurant = db.relationship('Restaurant', backref='reservations', lazy=True)
    table = db.relationship('Table', backref='reservations', lazy=True)

    # 🔗 Relación nueva
    dishes = db.relationship('Dish', secondary='reservation_dishes', backref='reservations')

# Modelo de categoría
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relación: una categoría tiene muchos platos
    dishes = db.relationship('Dish', backref='category', lazy=True)