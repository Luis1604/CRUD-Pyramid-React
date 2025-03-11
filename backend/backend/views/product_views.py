from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from backend.services.product_service import create_product, get_product_by_id, get_all_products, update_product, delete_product
from pyramid.request import Request

# Configuración para la vista de productos
@view_config(route_name='products', renderer='json', request_method='GET')
def list_products(request: Request):
    db = request.dbsession
    products = get_all_products(db)
    return {'products': [product.name for product in products]}

@view_config(route_name='product', renderer='json', request_method='GET')
def get_product(request: Request):
    db = request.dbsession
    product_id = request.matchdict['id']
    product = get_product_by_id(db, product_id)
    if product:
        return {'product': {'name': product.name, 'price': str(product.price), 'description': product.description}}
    return Response(status=404)

@view_config(route_name='product', renderer='json', request_method='POST')
def create_product_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description', None)
    
    product = create_product(db, name, price, description)
    return {'product': {'name': product.name, 'price': str(product.price), 'description': product.description}}

@view_config(route_name='product', renderer='json', request_method='PUT')
def update_product_view(request: Request):
    db = request.dbsession
    product_id = request.matchdict['id']
    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description', None)
    
    product = update_product(db, product_id, name, price, description)
    if product:
        return {'product': {'name': product.name, 'price': str(product.price), 'description': product.description}}
    return Response(status=404)

@view_config(route_name='product', renderer='json', request_method='DELETE')
def delete_product_view(request: Request):
    db = request.dbsession
    product_id = request.matchdict['id']
    product = delete_product(db, product_id)
    if product:
        return {'message': f'Product {product.name} deleted successfully'}
    return Response(status=404)
