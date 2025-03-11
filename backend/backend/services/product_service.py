from backend.models.product import Product
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pyramid_tm import transaction

def create_product(db: Session, name: str, price: float, description: str = None):
    # Verificar si el producto ya existe
    existing_product = db.query(Product).filter(Product.name == name).first()
    if existing_product:
        return {"error": "El producto ya existe"}

    # Crear un nuevo producto
    product = Product(name=name, price=price, description=description)
    db.add(product)
    
    try:
        transaction.manager.commit()  # Confirmar la transacción
        return product
    except IntegrityError:
        transaction.manager.abort()  # Hacer rollback en caso de error
        return {"error": "Error al crear el producto"}

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: int, name: str, price: float, description: str = None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None  # Indicar que el producto no existe

    product.name = name
    product.price = price
    product.description = description

    try:
        db.flush()   # Pyramid maneja la transacción, no uses transaction.manager.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()  # Revertir la transacción en caso de error
        return {"error": "Error al actualizar el producto"}


def delete_product(db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        transaction.commit()  # Usa transaction.commit() en vez de db.commit()
        return product
    return None
