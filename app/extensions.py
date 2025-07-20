from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis
from flask_migrate import Migrate

# Base de datos
db = SQLAlchemy()

# Autenticación
login_manager = LoginManager()
migrate = Migrate()

# Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
