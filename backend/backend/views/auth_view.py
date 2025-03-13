from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from pyramid.security import NO_PERMISSION_REQUIRED
from backend.services.auth_service import login_user
import logging
import json

# Configura el logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Ruta para iniciar sesión
@view_config(route_name='login', renderer='json', request_method='POST', permission=NO_PERMISSION_REQUIRED)
def login_view(request: Request):
    print("Solicitud POST recibida en /api/login") 
    db = request.dbsession
    try:
        email = request.json_body.get('email')
        password = request.json_body.get('password')
        # Intentar hacer login
        token = login_user(db, email, password)
        if token:
            print("Token generado", token)
            return Response(
                body=json.dumps({'token': token}),
                content_type='application/json',
                status=200
            )
        return Response(status=401, json_body={'error': 'Email o contraseña incorrectos'})
    except Exception as e:
        logger.error(f"Error en login_view: {e}")   
        return Response(status=500, json_body={'error': 'Error en el servidor'})


