from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from backend.services.auth_service import verify_jwt, create_response
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


