from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .meta import Base

class ActiveSessions(Base):
    __tablename__ = 'active_sessions'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.user_ext.id', ondelete="CASCADE"), nullable=False)  
    token = Column(String, nullable=False, unique=True)  # JWT generado
    ip_address = Column(String, nullable=False)  # Dirección IP del usuario
    device = Column(String, nullable=True)  # Nombre del dispositivo o User-Agent
    created_at = Column(DateTime, default=datetime.now())  # Fecha de inicio de sesión
    expires_at = Column(DateTime, nullable=False)  # Expiración del token
    is_active = Column(Boolean, default=True)  # Estado de la sesión
    user_ext = relationship('User_ext')

    def __init__(self, user_id, token, ip_address, device, duration_minutes=60):
        self.user_id = user_id
        self.token = token
        self.ip_address = ip_address
        self.device = device
        self.expires_at = datetime.now()() + timedelta(minutes=duration_minutes)


