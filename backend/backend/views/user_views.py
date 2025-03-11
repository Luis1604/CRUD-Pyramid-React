from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from backend.services.user_service import create_user, get_user_by_id, get_all_users, update_user, delete_user
from pyramid.request import Request

@view_config(route_name='users', renderer='json', request_method='GET')
def list_users(request: Request):
    db = request.dbsession
    users = get_all_users(db)
    return {'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]}

@view_config(route_name='user', renderer='json', request_method='GET')
def get_user(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = get_user_by_id(db, user_id)
    if user:
        return {'user': {'id': user.id, 'name': user.name, 'email': user.email}}
    return Response(status=404)

@view_config(route_name='user', renderer='json', request_method='POST')
def create_user_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    email = request.json_body.get('email')
    password = request.json_body.get('password')
    
    user = create_user(db, name, email, password)
    return {'user': {'id': user.id, 'name': user.name, 'email': user.email}}

@view_config(route_name='user', renderer='json', request_method='PUT')
def update_user_view(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    name = request.json_body.get('name')
    email = request.json_body.get('email')
    password = request.json_body.get('password')
    
    user = update_user(db, user_id, name, email, password)
    if user:
        return {'user': {'id': user.id, 'name': user.name, 'email': user.email}}
    return Response(status=404)

@view_config(route_name='user', renderer='json', request_method='DELETE')
def delete_user_view(request: Request):
    db = request.dbsession
    user_id = request.matchdict['id']
    user = delete_user(db, user_id)
    if user:
        return {'message': f'User {user.name} deleted successfully'}
    return Response(status=404)
