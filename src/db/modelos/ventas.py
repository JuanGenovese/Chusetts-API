from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class TurnosCaja(Base):
    __tablename__ = "TURNOS_CAJA"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("USUARIOS.id"), nullable=False)
    fecha_desde = Column(DateTime, nullable=False)
    fecha_hasta = Column(DateTime, nullable=True)
    efectivo_inicial = Column(Float, nullable=False, default=0.0)
    observacion_apertura = Column(String(100), nullable=False)
    observacion_cierre = Column(String(100), nullable=True)

    usuario = relationship("Usuarios", back_populates="turnos")
    movimientos = relationship("MovimientosVentas", back_populates="turno")

class Cupones(Base):
    __tablename__ = "CUPONES"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), nullable=False, unique=True)
    valor = Column(Float, nullable=False)
    fecha_desde = Column(Date, nullable=False)
    fecha_hasta = Column(Date, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    usuarios_asignados = relationship("CuponesUsuario", back_populates="cupon")

class CuponesUsuario(Base):
    __tablename__ = "CUPONES_USUARIO"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("USUARIOS.id"), nullable=False)
    cupon_id = Column(Integer, ForeignKey("CUPONES.id"), nullable=False)
    fecha_asignacion = Column(DateTime, nullable=False)

    usuario = relationship("Usuarios", back_populates="cupones")
    cupon = relationship("Cupones", back_populates="usuarios_asignados")
    movimiento_venta = relationship("MovimientosVentas", back_populates="cupon_usuario", uselist=False)

class Productos(Base):
    __tablename__ = "PRODUCTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    precio_venta = Column(Float, nullable=False)
    costo_unitario = Column(Float, nullable=False)
    stock_minimo = Column(Float, nullable=False, default=0.0)
    valor_puntos = Column(Integer, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    composiciones = relationship("ProductoComposicion", back_populates="producto")

class ProductoXMovimiento(Base):
    __tablename__ = "PRODUCTOS_X_MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_movimiento_venta = Column(Integer, ForeignKey("MOVIMIENTOS_VENTAS.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("PRODUCTOS.id"), nullable=False)
    cantidad_producto = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

    movimiento_venta = relationship("MovimientosVentas", back_populates="productos")
    producto = relationship("Productos")