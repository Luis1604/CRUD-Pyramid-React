from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from backend.services.user_service import create_user, get_user_by_id, get_all_users, delete_user
from pyramid.request import Request


# Listar todos los usuarios
@view_config(route_name='listusers', renderer='json', request_method='GET')
def list_users(request: Request):
    db = request.dbsession
    users = get_all_users(db)
    return {'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]}

# Obtener un usuario por ID
@view_config(route_name='user', renderer='json', request_method='GET')
def get_user(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = get_user_by_id(db, user_id)
    if user:
        return {'user': {'id': user.id, 'name': user.name, 'email': user.email}}
    return Response(status=404)

# Crear un nuevo usuario
@view_config(route_name='createuser', renderer='json', request_method='POST')
def create_user_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    email = request.json_body.get('email')
    password_hash = request.json_body.get('password')  # Encriptar la contraseña

    user = create_user(db, name, email, password_hash)
    return {'user': {'id': user.id, 'name': user.name, 'email': user.email}}



# Eliminar un usuario por ID
@view_config(route_name='user', renderer='json', request_method='DELETE')
def delete_user_view(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = delete_user(db, user_id)
    if user:
        return {'message': f'User {user.name} eliminado con exito'}
    return Response(status=404, json_body={'error': 'Producto no encontrado'})
