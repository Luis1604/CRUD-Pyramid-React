# models/order_product.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

class OrderProduct(Base):
    __tablename__ = 'order_products'
    __table_args__ = {'schema': 'public'}

    order_id = Column(Integer, ForeignKey('public.orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('public.products.id'), primary_key=True)

    # Relación con el pedido
    order = relationship("Order", back_populates="products")
    
    # Relación con el producto
    product = relationship("Product", back_populates="orders")
