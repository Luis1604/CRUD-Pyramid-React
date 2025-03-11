from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.models.user import User
import os

# Configuración de la base de datos (ajusta la URL según tu configuración)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://luix:AmtpfxfUDnd45euR57fVExecpOtRovEk@dpg-cv32jf0fnakc738h5flg-a.oregon-postgres.render.com/crudbd")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def crear_usuario_admin():
    email_admin = "luisbravo1604@gmail.com"
    nombre_admin = "Luis Bravo"
    password_admin = "@lux246810"

    # Verificar si el usuario ya existe
    admin_existente = session.query(User).filter_by(email=email_admin).first()
    if admin_existente:
        print("❌ El usuario administrador ya existe.")
        return

    # Crear el usuario administrador
    nuevo_admin = User(
        name=nombre_admin,
        email=email_admin,
        hashed_password=User.set_password(password_admin)
    )

    # Guardar en la base de datos
    session.add(nuevo_admin)
    session.commit()
    print("✅ Usuario administrador creado con éxito.")

if __name__ == "__main__":
    crear_usuario_admin()