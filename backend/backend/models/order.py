from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.users.id'), nullable=True)
    user_ext_id = Column(Integer, ForeignKey('public.user_ext.id'), nullable=True)

    # Relación con el usuario
    user = relationship("User", back_populates="orders")

    userext = relationship("User_ext", back_populates="orders")
    
    # Relación con los productos a través de la tabla intermedia order_products
    products = relationship("OrderProduct", back_populates="order")
