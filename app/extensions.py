from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis

# Base de datos
db = SQLAlchemy()

# Autenticación
login_manager = LoginManager()

# Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
