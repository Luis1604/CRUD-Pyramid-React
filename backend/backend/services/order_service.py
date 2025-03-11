from backend.models.order import Order
from backend.models.order_product import OrderProduct
from sqlalchemy.orm import Session

def create_order(db: Session, user_id: int, product_ids: list):
    order = Order(user_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for product_id in product_ids:
        order_product = OrderProduct(order_id=order.id, product_id=product_id)
        db.add(order_product)
    
    db.commit()
    return order

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session):
    return db.query(Order).all()

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order
