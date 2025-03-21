from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from backend.services.product_service import create_product, get_product_by_id, get_all_products, update_product, delete_product
from backend.services.auth_service import create_response
import logging

logger = logging.getLogger(__name__)

#Listar Productos
@view_config(route_name='products', renderer='json', request_method='GET')
def list_products(request: Request):
    db = request.dbsession
    products = get_all_products(db)
    logger.info("GET productos.")
    return create_response ({'products': [{'name': product.name, 'price': str(product.price), 'description': product.description} for product in products], "success": True }, 200)


#Obtener Producto
@view_config(route_name='product', renderer='json', request_method='GET')
def get_product(request: Request):
    db = request.dbsession
    product_id = request.matchdict['id']
    product = get_product_by_id(db, product_id)
    if product:
        return create_response({"product": {'name': product.name, 'description': product.description, 'price': str(product.price)}, "success": True }, 200)
    return create_response({"error": 'Producto no encontrado', "success": False}, 404)

#Crear Producto
@view_config(route_name='createproduct', renderer='json', request_method='POST')
def create_product_view(request: Request):
    db = request.dbsession
    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description')
    logger.info(f"Datos producto recibido: nombre {name}")
    product = create_product(db, name, price, description)
    if product is None:
        return create_response({"error": "Error al crear producto", "success": False}, 404)
    
    return create_response({"product": {'name': product.name, 
                                       'price': product.price, 
                                       'description': product.description}, 
                                       "success": True, 
                                       "message":"Producto creado con exito."}, 200)

#Actualizar Producto
@view_config(route_name='product', renderer='json', request_method='PUT')
def update_product_view(request: Request):
    db = request.dbsession
    try:
        product_id = int(request.matchdict['id'])
    except ValueError:
        logger.error("ID del producto invalido.")
        return create_response({"error": "ID del producto invalido.", "success": False}, 404)

    name = request.json_body.get('name')
    price = request.json_body.get('price')
    description = request.json_body.get('description')
    
    product = update_product(db, product_id, name, price, description)

    if product is None:
        return create_response({"error": "Producto no encontrado.", "success": False}, 404)

    return create_product({'product': {'name': product.name,'price': str(product.price),'description': product.description}, 
                           "success": True, 
                           "message":"Producto actualizado con exito."}, 200)


# Eliminar producto
@view_config(route_name='product', renderer='json', request_method='DELETE')
def delete_product_view(request):
    db = request.dbsession
    product_id = request.matchdict.get('id')

    product = delete_product(db, product_id)
    if product is None:
        logger.error("Producto no encontrado")
        return create_response({"error": "Producto no encontrado.", "success": False}, 404)
    
    return create_product({"success": True, 
                           "message":"Producto eliminado con exito."}, 200)

