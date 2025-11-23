from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Verificar si existe el usuario 1
    user = User.query.get(1)
    if not user:
        print("⚠️ Usuario 1 no existe. Creándolo...")
        new_user = User(
            email="admin@test.com",
            username="admin",
            password="password123", # En un caso real, usa set_password
            first_name="Admin",
            last_name="User"
        )
        # Forzar ID 1 para que coincida con tu Frontend hardcodeado
        new_user.id = 1 
        db.session.add(new_user)
        db.session.commit()
        print("✅ Usuario Admin creado con ID 1.")
    else:
        print("✅ El usuario 1 ya existe. Todo en orden.")