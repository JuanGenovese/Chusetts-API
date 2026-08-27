from src.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

class UsuarioAdm(Base):
    __tablename__ = "USUARIOS_ADM"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(50), unique=True, nullable=False)
    rol_adm_id = Column(Integer, ForeignKey("ROLES_ADM.id"), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    role = relationship("RoleAdm", back_populates="usuarios")
    turnos = relationship("TurnoCaja", back_populates="usuario_adm")

class RoleAdm(Base):
    __tablename__ = "ROLES_ADM"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rol = Column(String(25), unique=True, nullable=False)

    usuarios = relationship("UsuarioAdm", back_populates="role")
    
class UsuarioCli(Base):
    __tablename__ = "USUARIOS_CLI"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rol_cli_id = Column(Integer, ForeignKey("ROLES_CLI.id"), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(50), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(50), nullable=True)
    fecha_nac = Column(Date, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    role = relationship("RoleCli", back_populates="usuarios")
    puntos = relationship("Punto", back_populates="usuario_cli")
    cupones = relationship("CuponUsuario", back_populates="usuario_cli")

class RoleCli(Base):
    __tablename__ = "ROLES_CLI"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rol = Column(String(25), unique=True, nullable=False)

    usuarios = relationship("UsuarioCli", back_populates="role")

class Puntos(Base):
    __tablename__ = "PUNTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_cli_id = Column(Integer, ForeignKey("USUARIOS_CLI.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)

    usuario_cli = relationship("UsuarioCli", back_populates="puntos")
