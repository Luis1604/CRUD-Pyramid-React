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
        return Response(json.dumps({"error": "Token inválido o expirado"}), status=401)

    return {"message": f"Bienvenido, {user_data['name']}!"}
