from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from backend.services.product_service import create_product, get_product_by_id, get_all_products, update_product, delete_product

#Listar Productos
@view_config(route_name='products', renderer='json', request_method='GET')
def list_products(request: Request):
    db = request.dbsession
    products = get_all_products(db)
    return {'products': [{'name': product.name, 'price': str(product.price), 'description': product.description} for product in products]}

#Obtener Producto
@view_config(route_name='product', renderer='json', request_method='GET')
def get_product(request: Request):
    db = request.dbsession
    product_id = request.matchdict['id']
    product = get_product_by_id(db, product_id)
    if product:
        return {'product': {'name': product.name, 'price': str(product.price), 'description': product.description}}
    return Response(status=404, json_body={'error': 'Producto no encontrado'})

#Crear Producto
@view_config(route_name='createproduct', renderer='json', request_method='POST')
def create_product_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description', None)
    
    product = create_product(db, name, price, description)
    if isinstance(product, dict) and product.get('error'):
        return Response(status=400, json_body=product)
    
    return {'product': {'name': product.name, 'price': str(product.price), 'description': product.description}}

#Actualizar Producto
@view_config(route_name='product', renderer='json', request_method='PUT')
def update_product_view(request: Request):
    db = request.dbsession
    try:
        product_id = int(request.matchdict['id'])  # Asegurar que sea entero
    except ValueError:
        return Response(status=400, json_body={'error': 'ID de producto inválido'})

    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description', None)
    
    product = update_product(db, product_id, name, price, description)

    if product is None:
        return Response(status=404, json_body={'error': 'Producto no encontrado'})

    if isinstance(product, dict) and product.get("error"):
        return Response(status=400, json_body=product)

    return {
        'product': {
            'name': product.name,
            'price': str(product.price),
            'description': product.description
        }
    }


# Eliminar producto
@view_config(route_name='product', renderer='json', request_method='DELETE')
def delete_product_view(request):
    db = request.dbsession
    product_id = request.matchdict.get('id')

    product = delete_product(db, product_id)
    if product:
        return {'message': f'Producto {product.name} eliminado correctamente'}
    return Response(status=404, json_body={'error': 'Producto no encontrado'})
