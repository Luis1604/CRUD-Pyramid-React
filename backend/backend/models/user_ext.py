from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .meta import Base

class User_ext(Base):
    __tablename__ = 'user_ext'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    id_ext = Column(String(255), nullable=False)

    # Para la autenticación de dos factores
    otp_secret = Column(String, nullable=True)
    is_2fa_enabled = Column(Boolean, default=False)

    # Relación con los pedidos
    orders = relationship("Order", back_populates="userext", lazy="dynamic")