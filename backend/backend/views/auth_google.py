import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pyramid.view import view_config
from pyramid.response import Response
from pyramid_tm import transaction
from backend.models import User_ext
from backend.services.auth_service import create_token
import logging
from sqlalchemy.exc import IntegrityError

GOOGLE_CLIENT_ID = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com"

logger = logging.getLogger(__name__)

@view_config(route_name="auth_google", request_method="POST", renderer="json")
def auth_google(request):
    try:
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

        bd = request.dbsession

        # Buscar usuario en la base de datos
        user = bd.query(User_ext).filter_by(email=user_email).first()
        
        if not user:
            try:
                logger.info(f"Creando nuevo usuario con email {user_email}")
                user = User_ext(email=user_email, name=user_name, id_ext=user_sub)
                bd.add(user)
                bd.flush()
                transaction.manager.commit()
            except IntegrityError as e:
                transaction.manager.abort()
                if "uq_user_ext_email" in str(e):  # Verificar si el error es por email duplicado
                    logger.warning(f"El usuario con email {user_email} ya existe.")
                    return create_response({"error": "El usuario ya existe", "success": False}, 409)
                logger.error("Error inesperado al guardar el usuario", exc_info=True)
                return create_response({"error": "Error interno", "success": False}, 500)

        # Generar token
        session_token = create_token(user)
        logger.info(f"Token generado para {user_email}")
        return create_response({
            "message": "Login exitoso",
            "success": True,
            "token": session_token,
            "email": user_email,
            "name": user_name,
        }, 200)

    except ValueError:
        logger.warning("Token de Google inválido")
        return create_response({"error": "Token inválido o expirado", "success": False}, 401)
    except Exception as e:
        logger.exception("Error inesperado en auth_google")
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
