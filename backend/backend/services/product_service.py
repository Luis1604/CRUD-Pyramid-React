from backend.models.product import Product
from sqlalchemy.orm import Session

def create_product(db: Session, name: str, price: float, description: str = None):
    product = Product(name=name, price=price, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: int, name: str, price: float, description: str = None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.name = name
        product.price = price
        product.description = description
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product
