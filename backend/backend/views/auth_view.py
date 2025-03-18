from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from pyramid.security import NO_PERMISSION_REQUIRED
from backend.services.auth_service import login_user
import logging
import json

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@view_config(route_name="login", renderer="json", request_method="POST", permission=NO_PERMISSION_REQUIRED)
def login_view(request: Request):
    logger.info("Solicitud de inicio de sesión recibida en /api/login")
    
    db = request.dbsession
    try:
        data = request.json_body
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            logger.warning("Intento de login sin credenciales")
            return Response(json_body={"error": "Faltan credenciales"}, status=400)

        token = login_user(db, email, password)
        if token:
            logger.info(f"Inicio de sesión exitoso para {email}")
            return Response(json_body={"token": token}, status=200)

        logger.warning(f"Intento de inicio de sesión fallido para {email}")
        return Response(json_body={"error": "Email o contraseña incorrectos"}, status=401)

    except json.JSONDecodeError:
        logger.error("Solicitud inválida: se esperaba JSON")
        return Response(json_body={"error": "Solicitud inválida, se esperaba JSON"}, status=400)
    
    except Exception as e:
        logger.exception("Error inesperado en login_view")
        return Response(json_body={"error": "Error interno del servidor"}, status=500)
