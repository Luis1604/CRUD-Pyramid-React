from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Numeric, nullable=False)

    # Relación con los pedidos a través de la tabla intermedia order_products
    orders = relationship("OrderProduct", back_populates="product")
