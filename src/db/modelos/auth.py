from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base, TimestampMixin

class CuentaAuth(Base, TimestampMixin):
    __tablename__ = "CUENTAS"
    __table_args__ = {"schema": "auth"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuarios", back_populates="cuenta", uselist=False)