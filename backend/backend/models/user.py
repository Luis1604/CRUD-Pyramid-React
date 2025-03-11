from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .meta import Base
import bcrypt

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Almacenar la contraseña encriptada

    # Relación con los pedidos
    orders = relationship("Order", back_populates="user", lazy="dynamic")

    # Método para verificar si la contraseña ingresada es válida
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    # Método para establecer la contraseña encriptada
    def set_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
