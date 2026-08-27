from src.db.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class MedioPago(Base):
    __tablename__ = "MEDIOS_PAGO"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medio_pago = Column(String(20), unique=True, nullable=False)

    movimientos = relationship("MediosPagoxMovimiento", back_populates="medio_pago")

class MediosPagoxMovimiento(Base):
    __tablename__ = "MEDIOS_PAGO_X_MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey("MOVIMIENTOS.id"), nullable=False)
    id_medio_pago = Column(Integer, ForeignKey("MEDIOS_PAGO.id"), nullable=False)
    monto = Column(Float, nullable=False)

    movimiento = relationship("Movimiento", back_populates="medios_pago")
    medio_pago = relationship("MedioPago", back_populates="movimientos")

class Movimiento(Base):
    __tablename__ = "MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_id = Column(Integer, ForeignKey("TIPOS_MOVIMIENTOS.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)

    tipo = relationship("TiposMovimientos", back_populates="movimientos")
    medios_pago = relationship("MediosPagoxMovimiento", back_populates="movimiento")
    venta = relationship("MovimientoVentas", back_populates="movimiento", uselist=False)
    compra = relationship("MovimientoCompra", back_populates="movimiento", uselist=False)
    gasto = relationship("MovimientoGasto", back_populates="movimiento", uselist=False)

class TiposMovimientos(Base):
    __tablename__ = "TIPOS_MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(20), unique=True, nullable=False)

    movimientos = relationship("Movimiento", back_populates="tipo")

class MovimientoVentas(Base):
    __tablename__ = "MOVIMIENTOS_VENTAS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movimiento_id = Column(Integer, ForeignKey("MOVIMIENTOS.id"), unique=True, nullable=False)
    turno_caja_id = Column(Integer, ForeignKey("TURNOS_CAJA.id"), nullable=False)
    monto_total = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)

    movimiento = relationship("Movimiento", back_populates="venta")
    turno = relationship("TurnoCaja", back_populates="movimientos")
    productos = relationship("ProductoXMovimiento", back_populates="movimiento_venta")
    cupon_usuario = relationship("CuponUsuario", back_populates="movimiento_venta")

class MovimientoCompra(Base):
    __tablename__ = "MOVIMIENTOS_COMPRA"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey("MOVIMIENTOS.id"), unique=True, nullable=False)
    fecha = Column(DateTime, nullable=False)
    costo_total = Column(Float, nullable=False)
    detalle = Column(String(100), nullable=True)

    movimiento = relationship("Movimiento", back_populates="compra")
    stock_items = relationship("StockXMovimiento", back_populates="compra")

class MovimientoGasto(Base):
    __tablename__ = "MOVIMIENTOS_GASTO"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movimiento_id = Column(Integer, ForeignKey("MOVIMIENTOS.id"), unique=True, nullable=False)
    concepto = Column(String(150), nullable=False)
    cantidad = Column(Float, nullable=True)
    importe = Column(Float, nullable=False)
    detalle = Column(String(100), nullable=True)

    movimiento = relationship("Movimiento", back_populates="gasto")