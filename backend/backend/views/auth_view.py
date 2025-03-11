from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from pyramid.security import NO_PERMISSION_REQUIRED
from backend.services.auth_service import login_user
from backend.services.user_service import create_user
from backend.models import User
from sqlalchemy.orm import Session

# Ruta para iniciar sesión
@view_config(route_name='login', renderer='json', request_method='POST', permission=NO_PERMISSION_REQUIRED)
def login_view(request: Request):
    db = request.dbsession
    email = request.json_body.get('email')
    password = request.json_body.get('password')

    # Intentar hacer login
    token = login_user(db, email, password)
    if token:
        return {'access_token': token}
    return Response(status=401, json_body={'error': 'Email o contraseña incorrectos'})


