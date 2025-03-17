from pyramid.security import NO_PERMISSION_REQUIRED
import json
from pyramid.view import view_config
from pyramid.response import Response
from backend.services.auth_service import verify_jwt

@view_config(route_name="dashboard", request_method="GET", permission=NO_PERMISSION_REQUIRED, renderer="json")
def dashboard(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(json.dumps({"error": "No autorizado"}), status=401)

    token = auth_header.split(" ")[1]
    user_data = verify_jwt(token)

    if not user_data:
        return create_response({"error": "Token inválido o expirado"}, 401)

    return create_response({"message": f"Bienvenido, {user_data['name']}!"}, 200)

def create_response(data, status_code):
    """ Genera una respuesta JSON con las cabeceras adecuadas """
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response
