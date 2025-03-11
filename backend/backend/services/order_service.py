from backend.models.order import Order
from backend.models.order_product import OrderProduct
from sqlalchemy.orm import Session
from pyramid_tm import transaction

def create_order(db: Session, user_id: int, product_ids: list):
    # Crear la nueva orden
    order = Order(user_id=user_id)
    db.add(order)
    db.flush() 
    db.refresh(order)
    print("ID order",order.id)

    # Ahora que la orden tiene un ID, agregamos los productos
    for product_id in product_ids:
        order_product = OrderProduct(order_id=order.id, product_id=product_id)
        db.add(order_product)
    
    # Commit final después de agregar los productos
    transaction.manager.commit()

    # La orden ya tiene todos los productos asociados, la retornamos
    return order

def get_order_by_id(db: Session, order_id: int):
    # Obtener una orden por ID
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session):
    # Obtener todas las órdenes
    return db.query(Order).all()

def delete_order(db: Session, order_id: int):
    # Eliminar una orden por ID
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        transaction.manager.commit()  # Confirmar la transacción después de eliminar la orden
    return order
