import json
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pyramid.view import view_config
from pyramid.response import Response
from backend.models import User
from backend.services.auth_service import create_token

GOOGLE_CLIENT_ID = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com"

@view_config(route_name="auth_google", request_method="POST", renderer="json")
def auth_google(request):
    try:
        data = request.json_body
        token = data.get("token")

        # Verificar el token de Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

        # Extraer datos del usuario
        user_email = idinfo["email"]
        user_name = idinfo.get("name", "")

        # Buscar o registrar al usuario en la base de datos (esto es un ejemplo)
        user = request.dbsession.query(User).filter_by(email=user_email).first()
        if not user:
            user = User(email=user_email, name=user_name)
            request.dbsession.add(user)

        # Crear un token JWT para la sesión
        jwt_token = create_token(user)

        return {"success": True, "token": jwt_token}

    except Exception as e:
        return Response(json.dumps({"success": False, "error": str(e)}), status=400)
