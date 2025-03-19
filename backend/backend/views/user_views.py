from pyramid.view import view_config
from pyramid.response import Response
from backend.services.user_service import create_user, get_user_by_id, get_all_users, delete_user
from pyramid.request import Request
import json
import logging

logger = logging.getLogger(__name__)

# Listar todos los usuarios
@view_config(route_name='listusers', renderer='json', request_method='GET')
def list_users(request: Request):
    db = request.dbsession
    users = get_all_users(db)
    return create_response({'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]}, 200)

# Obtener un usuario por ID
@view_config(route_name='user', renderer='json', request_method='GET')
def get_user(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = get_user_by_id(db, user_id)
    if user:
        logger.info(f"Usuario encontrado: {user['name']}")
        return create_response({'id': user['id'], 'name': user['name'], 'email': user['email']}, 200)

    return create_response({'success': False, 'error': 'Usuario no encontrado'}, 404)

# Crear un nuevo usuario
@view_config(route_name='createuser', renderer='json', request_method='POST')
def create_user_view(request: Request):
    logger.info("Creando un nuevo usuario")
    db = request.dbsession
    name = request.json_body.get('name')
    email = request.json_body.get('email')
    password_hash = request.json_body.get('password')

    newuser = create_user(db, name, email, password_hash)
    if newuser == None:
        logger.error("Error al crear usuario")
        return create_response({'success': False,'error': 'Error al crear usuario'}, 400)
    else:
        logger.info(f"Usuario creado: {newuser.name}")
        return create_response({'success': True,'message': 'Usuario registrado con exito','user': {'name': newuser.name,'email': newuser.email}}, 400)

# Eliminar un usuario por ID
@view_config(route_name='user', renderer='json', request_method='DELETE')
def delete_user_view(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = delete_user(db, user_id)
    if user:
        return create_response({'success': True, 'message': 'Usuario eliminado con éxito'}, 200)
    return create_response({'success': False, 'error': 'Usuario no encontrado'}, 404)


def create_response(data, status_code):
    response = Response(json.dumps(data), content_type="application/json; charset=utf-8", status=status_code)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true"
    })
    return response
