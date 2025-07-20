from app import create_app
from app.models.db import db, User

app = create_app()

with app.app_context():
    # Crear tablas si no existen
    db.create_all()
    
    # Crear/actualizar admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@uce.edu.ec',
            role='admin'
        )
        db.session.add(admin)
    
    # FORZAR la contraseña correcta (asegurando coherencia)
    admin.set_password('admin123')  # Ahora sí será admin123
    db.session.commit()
    print("✅ Usuario admin actualizado: usuario=admin, contraseña=admin123")