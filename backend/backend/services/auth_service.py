import bcrypt
import jwt
import datetime
from backend.models.user import User
import logging
from sqlalchemy.orm import Session
from pyramid.threadlocal import get_current_registry
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# Obtener los valores de configuración del archivo INI
def get_jwt_config():
    config = get_current_registry().settings
    jwt_secret_key = config.get('JWT_SECRET_KEY')
    jwt_algorithm = config.get('JWT_ALGORITHM')
    return jwt_secret_key, jwt_algorithm


# Cifrar una contraseña
def encrypt_password(password: str) -> bytes:
    config = get_current_registry().settings
    key = config.get('KEY')
    cipher = Fernet(key)
    return cipher.encrypt(password.encode())

# Descifrar una contraseña
def decrypt_password(encrypted_password: bytes) -> str:
    config = get_current_registry().settings
    key = config.get('KEY')
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password).decode()

# Función para encriptar la contraseña
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Función para verificar la contraseña
def verify_password(stored_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

# Función para crear el token JWT
def create_token(user: User) -> str:
    jwt_secret_key, jwt_algorithm = get_jwt_config()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiración de 1 hora
    logging.info(f"Expiracion: {expiration}")
    payload = {
        "sub": str(user.id),  # ID del usuario como "sub" (subject)
        "exp": expiration,  # Expiración del token
        "name": user.name,  # Puedes agregar más datos si es necesario
        "email": user.email
    }

    # Codificación a bytes
    token = jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)  # Crea el token
    return token

# Función para obtener el usuario por correo electrónico
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Función para iniciar sesión
def login_user(db: Session, email: str, password: str):
    """
    Función para autenticar un usuario y generar un token si las credenciales son correctas.
    """
    user = get_user_by_email(db, email)
    if not user:
        logger.warning(f"Usuario no encontrado: {email}")
        return None

    if not verify_password(user.hashed_password, password):
        logger.warning(f"Contraseña incorrecta para usuario: {email}")
        return None

    token = create_token(user)
    logger.info(f"Token generado correctamente para {email}")
    return token


def verify_jwt(token: str):
    jwt_secret_key, jwt_algorithm = get_jwt_config()
    try:
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        
        # Verificar si el token tiene la propiedad 'sub', que es el identificador del usuario
        if 'sub' not in decoded_token:
            logging.warning("Token inválido, falta el subject")
            return {"error": "Token inválido, falta el subject"}

        return decoded_token  # Retornamos el payload decodificado

    except ExpiredSignatureError:
        logging.warning("Token expirado")
        return {"error": "Token expirado"}
    
    except InvalidTokenError:
        logging.warning("Token inválido")
        return {"error": "Token inválido"}
    
    except Exception as e:
        logging.exception(f"Error al verificar el token: {str(e)}")
        return {"error": f"Error inesperado: {str(e)}"}

    
    
