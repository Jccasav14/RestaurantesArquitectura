import os

class Config:
    #Clave secreta para sesiones
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    #URL de conexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/restaurante')
    #Desactiva el seguimiento de modificaciones en SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Carpeta para guardar archivos subidos (imágenes de restaurantes o platos)
    UPLOAD_FOLDER = 'app/static/uploads'
    #Tipos de archivos permitidos al subir imágenes
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    #Configuración de conexión a Redis (host, puerto y base de datos)
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 0)