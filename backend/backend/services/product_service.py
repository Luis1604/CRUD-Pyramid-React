from backend.models.product import Product
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pyramid_tm import transaction

logger = logging.getLogger(__name__)

def create_product(db: Session, name: str, price: str, description: str):
    # Verificar si el producto ya existe
    existing_product = db.query(Product).filter(Product.name == name).first()
    if existing_product:
        logging.error("El producto ya existe")
        return None

    product = Product(name=name, price=price, description=description)
    try:
        logging.info(f"Creando producto {product.name}, {product.description}, {product.price}")
        db.add(product)
        db.flush()
        transaction.manager.commit() 
        logging.info("Producto creado con exito...")
        return product
    except IntegrityError:
        transaction.manager.abort()
        logging.error("Error al crear el producto.")
        return None

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: int, name: str, price: float, description: str = None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.error("Producto no encontrado.")
        return None

    product.name = name
    product.price = price
    product.description = description

    try:
        db.flush()   # Pyramid maneja la transacción, no uses transaction.manager.commit()
        db.refresh(product)
        logger.inf(f"Producto {product.name} actualizado con exito.")
        return product
    except IntegrityError:
        db.rollback()
        logger.error("Error al actualizar producto en bd.")
        return None


def delete_product(db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        transaction.commit()
        logger.inf(f"Producto {product.name} eliminado con exito.")
        return product
    return None
