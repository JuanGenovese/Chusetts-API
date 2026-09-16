from sqlalchemy import true
from src.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "USUARIOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuenta_id = Column(Integer, ForeignKey("auth.CUENTAS.id", ondelete="CASCADE"), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(50), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(50), nullable=True)
    fecha_nac = Column(Date, nullable=False)
    rol_id = Column(Integer, ForeignKey("ROLES.id"), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    cuenta = relationship("CuentaAuth", back_populates="usuarios")
    role = relationship("Roles", back_populates="usuarios")
    turnos = relationship("TurnosCaja", back_populates="usuario")
    puntos = relationship("Puntos", back_populates="usuario")
    cupones = relationship("CuponesUsuario", back_populates="usuario")

class Roles(Base):
    __tablename__ = "ROLES"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rol = Column(String(25), unique=True, nullable=False)

    usuarios = relationship("Usuarios", back_populates="role")


class Puntos(Base):
    __tablename__ = "PUNTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("USUARIOS.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    usuario = relationship("Usuarios", back_populates="puntos")
