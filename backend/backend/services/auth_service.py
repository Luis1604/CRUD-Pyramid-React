import bcrypt
import jwt
import datetime
from backend.models.user import User
from sqlalchemy.orm import Session
from pyramid.threadlocal import get_current_registry

# Obtener los valores de configuración del archivo INI
def get_jwt_config():
    config = get_current_registry().settings
    jwt_secret_key = config.get("YjMtEbnW4WQQZJLAsTwOvqWBMuRHhaOGV1LEyL3Pwco=")
    jwt_algorithm = config.get("HS256")
    return jwt_secret_key, jwt_algorithm

# Función para encriptar la contraseña
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Función para verificar la contraseña
def verify_password(stored_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

# Función para crear el token JWT
def create_token(user: User) -> str:
    jwt_secret_key, jwt_algorithm = get_jwt_config()  # Obtiene la clave secreta y el algoritmo
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiración de 1 hora
    payload = {
        "sub": user.id,  # ID del usuario como "sub" (subject)
        "exp": expiration  # Expiración del token
    }
    token = jwt.PyJWT().encode(payload, "YjMtEbnW4WQQZJLAsTwOvqWBMuRHhaOGV1LEyL3Pwco", "HS256")  # Crea el token
    return token

# Función para obtener el usuario por correo electrónico
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Función para iniciar sesión
def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(user.hashed_password, password):  # Asegúrate de que el nombre del campo sea correcto
        token = create_token(user)  # Si el usuario es válido, crea el token
        return token
    return None  # Si no se encuentra el usuario o la contraseña no es válida, devuelve None
