from pyramid.security import NO_PERMISSION_REQUIRED
import json
from pyramid.view import view_config
from pyramid.response import Response
from backend.services.auth_service import verify_jwt
import logging

logger = logging.getLogger(__name__)

@view_config(route_name="dashboard", request_method="GET", permission=NO_PERMISSION_REQUIRED, renderer="json")
def dashboard(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logging.warning("No se recibió token de autorización")
        return create_response({"error": "No autorizado"}, 401)

    token = auth_header.split(" ")[1]
    user_data = verify_jwt(token)
    if 'sub' in user_data:
        logging.info(f"Token verificado")
        return create_response({"message": f"Bienvenido... ","success": True, "name": user_data['name']}, 200)
    
    return create_response({"error": "Error validar token","success": False}, 400)


def create_response(data, status_code):
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response
