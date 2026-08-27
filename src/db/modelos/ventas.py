from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class TurnoCaja(Base):
    __tablename__ = "TURNOS_CAJA"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_adm_id = Column(Integer, ForeignKey("USUARIOS_ADM.id"), nullable=False)
    fecha_desde = Column(DateTime, nullable=False)
    fecha_hasta = Column(DateTime, nullable=True)
    abierto = Column(Boolean, nullable=False, default=True)
    efectivo_inicial = Column(Float, nullable=False, default=0.0)
    observacion_apertura = Column(String(100), nullable=False)
    observacion_cierre = Column(String(100), nullable=True)

    usuario_adm = relationship("UsuarioAdm", back_populates="turnos")
    movimientos = relationship("MovimientoVentas", back_populates="turno")

class Cupon(Base):
    __tablename__ = "CUPONES"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), nullable=False, unique=True)
    valor = Column(Float, nullable=False)
    fecha_desde = Column(Date, nullable=False)
    fecha_hasta = Column(Date, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    usuarios_asignados = relationship("CuponUsuario", back_populates="cupon")

class CuponUsuario(Base):
    __tablename__ = "CUPONES_USUARIO"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_cli_id = Column(Integer, ForeignKey("USUARIOS_CLI.id"), nullable=False)
    cupon_id = Column(Integer, ForeignKey("CUPONES.id"), nullable=False)
    movimiento_venta_id = Column(Integer, ForeignKey("MOVIMIENTOS_VENTAS.id"), nullable=True)
    disponible = Column(Boolean, default=True, nullable=False)

    usuario_cli = relationship("UsuarioCli", back_populates="cupones")
    cupon = relationship("Cupon", back_populates="usuarios_asignados")
    movimiento_venta = relationship("MovimientoVentas", back_populates="cupon_usuario")

class Producto(Base):
    __tablename__ = "PRODUCTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    valor_puntos = Column(Integer, nullable=True)
    nombre = Column(String(150), nullable=False)
    precio_venta = Column(Float, nullable=False)
    costo_unitario = Column(Float, nullable=False)
    stock_minimo = Column(Float, nullable=False, default=0.0)
    activo = Column(Boolean, default=True, nullable=False)

    composiciones = relationship("ProductoComposicion", back_populates="producto")

class ProductoXMovimiento(Base):
    __tablename__ = "PRODUCTOS_X_MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_movimiento_venta = Column(Integer, ForeignKey("MOVIMIENTOS_VENTAS.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("PRODUCTOS.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

    movimiento_venta = relationship("MovimientoVentas", back_populates="productos")
    producto = relationship("Producto")