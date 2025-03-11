from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from backend.services.order_service import create_order, get_order_by_id, get_all_orders, delete_order
from pyramid.request import Request

# Listar todas las órdenes
@view_config(route_name='orders', renderer='json', request_method='GET')
def list_orders(request: Request):
    db = request.dbsession
    orders = get_all_orders(db)
    return {'orders': [{'id': order.id, 'user_id': order.user_id} for order in orders]}

# Obtener una orden por ID
@view_config(route_name='order', renderer='json', request_method='GET')
def get_order(request: Request):
    db = request.dbsession
    order_id = request.matchdict['id']
    order = get_order_by_id(db, order_id)
    
    if order:
        # Incluir los productos asociados
        return {
            'order': {
                'id': order.id,
                'user_id': order.user_id,
                'products': [op.product_id for op in order.products]
            }
        }
    return Response(status=404)

# Crear una nueva orden
@view_config(route_name='orders', renderer='json', request_method='POST')
def create_order_view(request: Request):
    db = request.dbsession
    user_id = request.json_body.get('user_id')
    product_ids = request.json_body.get('product_ids', [])

    if not user_id or not product_ids:
        return Response(
            json_body={"error": "user_id and product_ids are required"},
            status=400
        )

    order = create_order(db, user_id, product_ids)
    # Incluir los productos asociados al devolver la orden
    return {
        'order': {
            'id': order.id,
            'user_id': order.user_id,
            'products': [op.product_id for op in order.products]
        }
    }

# Eliminar una orden por ID
@view_config(route_name='order', renderer='json', request_method='DELETE')
def delete_order_view(request: Request):
    db = request.dbsession
    order_id = request.matchdict['id']
    order = delete_order(db, order_id)
    
    if order:
        return {'message': f'Order {order.id} deleted successfully'}
    return Response(status=404)
