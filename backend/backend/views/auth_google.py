import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pyramid.view import view_config
from pyramid_tm import transaction
from sqlalchemy.exc import IntegrityError
from backend.models import User_ext
from backend.services.auth_service import create_token
import logging
from pyramid.response import Response

logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com"

@view_config(route_name="auth_google", request_method="POST", renderer="json")
def auth_google(request):
    bd = request.dbsession
    logger.info("Solicitud de inicio de sesión con Google")
    try:
        data = request.json_body
        token = data.get("token")

        if not token:
            response_data = {"error": "Token no recibido", "success": False}
            status_code = 400

        # Verificar el token de Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

        # Verificar que el token es de Google
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            logger.warning("Token no es de Google")
            response_data = {"error": "Token inválido", "success": False}
            status_code = 401
            return create_response(response_data, status_code)

        # Extraer datos del usuario
        user_sub = idinfo["sub"]  # ID único de Google
        user_email = idinfo["email"]
        user_name = idinfo.get("name", "")

        # Buscar usuario en la base de datos
        logger.info(f"Buscando usuario con email {user_email}")
        user = bd.query(User_ext).filter_by(email=user_email).first()

        if not user:
            # Si no existe, creamos el usuario
            try:
                logger.info(f"Creando nuevo usuario con email {user_email}")
                user = User_ext(email=user_email, name=user_name, id_ext=user_sub)
                bd.add(user)
                logger.info("Guardando usuario en la base de datos")
                transaction.manager.commit()
            except IntegrityError:
                logger.error("Error al guardar el usuario en la base de datos", exc_info=True)
                transaction.manager.abort()
                response_data = {"error": "Error al guardar el usuario", "success": False}
                status_code = 401
                return create_response(response_data, status_code)

        # Generar token
        session_token = create_token(user)
        logger.info(f"Token generado para {user_email}, {session_token}")
        response_data = {
            "message": "Login exitoso",
            "success": True,
            "token": session_token,
            "email": user_email,
            "name": user_name,
        }
        status_code = 200

    except ValueError:
        logger.warning("Token de Google inválido")
        response_data = {"error": "Token inválido o expirado", "success": False}
        status_code = 401
        return create_response(response_data, status_code)
    except Exception as e:
        logger.exception("Error inesperado en auth_google")
        response_data = {"error": str(e), "success": False}
        status_code = 500
        return create_response(response_data, status_code)


    return create_response(response_data, status_code)

def create_response(data, status_code):
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response