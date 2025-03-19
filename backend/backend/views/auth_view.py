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

        # Verificar que se reciban las credenciales
        if not email or not password:
            logger.warning("Intento de login sin credenciales")
            return create_response({"error": "Faltan credenciales"}, 400)
        
        token = login_user(db, email, password)
        
        # Si el token es generado, enviar respuesta de éxito
        if token:
            logger.info(f"Inicio de sesión exitoso para {email}")
            response_data = {
                "message": "Login exitoso",
                "success": True,
                "token": token,
                "email": email,
            }
            return create_response(response_data, 200)
        else:
            logger.warning(f"Intento de inicio de sesión fallido para {email}")
            return create_response({"error": "Email o contraseña incorrectos"}, 401)

    except json.JSONDecodeError:
        logger.error("Solicitud inválida: se esperaba JSON")
        return create_response({"error": "Solicitud inválida, se esperaba JSON"}, 400)
    
    except Exception as e:
        logger.exception("Error inesperado en login_view")
        return create_response({"error": "Error interno del servidor"}, 500)

    
def create_response(data, status_code):
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response