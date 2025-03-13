from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from backend.services.user_service import create_user, get_user_by_id, get_all_users, delete_user
from pyramid.request import Request
import json


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
        print("Usuario creado: ",user.name)
        return Response(
            body=json.dumps({'id': user['id'], 'name': user['name'], 'email': user['email']}), 
            content_type='application/json',
            status=200
        )
    return Response(status=404)

# Crear un nuevo usuario
@view_config(route_name='createuser', renderer='json', request_method='POST')
def create_user_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    email = request.json_body.get('email')
    password_hash = request.json_body.get('password')

    newuser = create_user(db, name, email, password_hash)
    print("Usuario creado respuesta:", newuser, "Tipo:", type(newuser))

    # Si es un diccionario, significa que hubo un error
    if isinstance(newuser, dict) and "error" in newuser:
        print("Error en el json")
        return Response(
            body=json.dumps(newuser), 
            content_type='application/json',
            status=400  # Bad Request si hay un error
        )

    print("JSON respuesta:", newuser)
    return Response(
        body=json.dumps({'message': 'Usuario registrado con éxito', 'name': newuser}),
        content_type='application/json; charset=utf-8',  # Aquí agregamos charset=utf-8
        status=200  # Aseguramos que sea 200 OK
    )


# Eliminar un usuario por ID
@view_config(route_name='user', renderer='json', request_method='DELETE')
def delete_user_view(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = delete_user(db, user_id)
    if user:
        return {'message': f'User {user.name} eliminado con exito'}
    return Response(status=404, json_body={'error': 'Producto no encontrado'})
