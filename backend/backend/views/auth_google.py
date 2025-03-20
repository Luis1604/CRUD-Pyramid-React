import json
import base64
import redis
import pyotp
from backend.models import User_ext
from backend.services.auth_service import create_token, encrypt_password, decrypt_password
from backend.services.user_service import send_email
import logging
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pyramid.view import view_config
from pyramid.response import Response
from pyramid_tm import transaction
from sqlalchemy.exc import IntegrityError
from pyramid.threadlocal import get_current_registry


GOOGLE_CLIENT_ID = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com"


logger = logging.getLogger(__name__)

@view_config(route_name="auth_google", request_method="POST", renderer="json")
def auth_google(request):
   
    data = request.json_body
    token = data.get("token")

    # Verificar el token de Google
    idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

    # Verificar que el token es de Google
    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        logger.warning("Token no es de Google")
        return create_response({"error": "Token inválido", "success": False}, 401)

    # Extraer datos del usuario
    user_email = idinfo["email"]
    user_name = idinfo.get("name", "")
    user_sub = idinfo["sub"]
    logger.info(f"Usuario autenticado: {user_email}")
    config = get_current_registry().settings
    redis_client = redis.StrictRedis(host=config.get('redis.host'), port=config.get('redis.port'), db=config.get('redis.db '), decode_responses=True)
    bd = request.dbsession
    
    # Buscar usuario en la base de datos
    user = bd.query(User_ext).filter_by(email=user_email).first()
    try:
        if not user:
            logger.info(f"Creando nuevo usuario con email {user_email}")
            opt = pyotp.random_base32()
            logger.info(f"Secret: {opt}")
            crypt = base64.urlsafe_b64encode(encrypt_password(opt)).decode()
            logger.info(f"Secret cifrado: {crypt}")
            user = User_ext(email=user_email, name=user_name, id_ext=user_sub, is_2fa_enabled=True, otp_secret=crypt)
            bd.add(user)
            bd.flush()
            transaction.manager.commit()
            session_token = create_token(user)
            totp = pyotp.TOTP(opt, interval=60, digits=6)
            opt = totp.now()
            redis_client.setex(f"totp:{user_email}", 300, opt)
            logger.info(f"Código OTP esperado para {user_email}: {opt}")
            return create_response({
                "message": "Login exitoso",
                "success": True,
                "token": session_token,
                "email": user_email,
                "name": user_name,
                "otp_required": user.is_2fa_enabled
            }, 200)
        else:
            logger.info(f"Usuario con email {user_email} ya existe")
            session_token = create_token(user)
            descrypt = base64.urlsafe_b64decode(user.otp_secret.encode())
            decoded_key = decrypt_password(descrypt)
            totp = pyotp.TOTP(decoded_key, interval=60, digits=6)
            opt = totp.now()
            redis_client.setex(f"totp:{user_email}", 300, opt)
            mail_sent = send_email(user_email, opt)
            if not mail_sent:
                logger.error("Error al enviar el correo electrónico")
                return create_response({"error": "Error al enviar el correo electrónico", "success": False}, 500)
            else:
                logger.info(f"Código OTP esperado para {user_email}: {opt}")
                return create_response({
                    "message": "Login exitoso",
                    "success": True,
                    "token": session_token,
                    "email": user_email,
                    "name": user_name,
                    "otp_required": user.is_2fa_enabled
                }, 200)
        
    except IntegrityError as e:
        transaction.manager.abort()
        if "uq_user_ext_email" in str(e):  # Verificar si el error es por email duplicado
            logger.warning(f"El usuario con email {user_email} ya existe.")
            return create_response({"error": "El usuario ya existe", "success": False}, 409)
        logger.error("Error inesperado al guardar el usuario", exc_info=True)
        return create_response({"error": "Error interno", "success": False}, 500)
    


@view_config(route_name="two_steps", request_method="POST", renderer="json")
def two_steps(request):
    try:
        data = request.json_body
        config = get_current_registry().settings
        redis_client = redis.StrictRedis(host=config.get('redis.host'), port=config.get('redis.port'), db=config.get('redis.db '), decode_responses=True)
        email = data.get("email")
        otp_code = data.get("otp_code")
        opt = redis_client.get(f"totp:{email}")
        bd = request.dbsession
        user = bd.query(User_ext).filter_by(email=email).first()
        if opt!=otp_code:
            logger.warning("Código 2FA inválido")
            return create_response({"error": "Código 2FA inválido", "success": False}, 401)
        else:
            session_token = create_token(user)
            logger.info(f"Token 2FK validado para {email}")
            return create_response({
                "message": "Validación 2FK exitosa",
                "success": True,
                "token": session_token,
                "email": email
            }, 200)
            
    except Exception as e:
        logger.exception("Error inesperado en two_steps")
        return create_response({"error": str(e), "success": False}, 500)


def create_response(data, status_code):
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response
