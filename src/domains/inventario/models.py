from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base


class Stock(Base):
    __tablename__ = "STOCK"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), unique=True, nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)
    cantidad_minima = Column(Integer, nullable=False, default=0)

    proveedores = relationship("StockXProveedor", back_populates="stock")
    usos_composicion = relationship("ProductoComposicion", back_populates="stock_item")
    movimientos_compra = relationship("StockXMovimiento", back_populates="stock")


class StockXMovimiento(Base):
    __tablename__ = "STOCK_X_MOVIMIENTOS"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mov_compra = Column(Integer, ForeignKey("MOVIMIENTOS_COMPRA.id"), nullable=False)
    id_stock = Column(Integer, ForeignKey("STOCK.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    costo_unitario = Column(Float, nullable=False)

    compra = relationship("MovimientoCompra", back_populates="stock_items")
    stock = relationship("Stock", back_populates="movimientos_compra")


class ProductoComposicion(Base):
    __tablename__ = "PRODUCTO_COMPOSICION"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("PRODUCTOS.id"), nullable=False)
    id_stock = Column(Integer, ForeignKey("STOCK.id"), nullable=False)
    cantidad_usada = Column(Float, nullable=False)

    producto = relationship("Producto", back_populates="composiciones")
    stock_item = relationship("Stock", back_populates="usos_composicion")


class Proveedor(Base):
    __tablename__ = "PROVEEDORES"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(50), nullable=True)
    mail = Column(String(150), nullable=True)
    localidad = Column(String(100), nullable=True)
    barrio = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True, nullable=True)

    stock_items = relationship("StockXProveedor", back_populates="proveedor")


class StockXProveedor(Base):
    __tablename__ = "STOCK_X_PROVEEDORES"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("PROVEEDORES.id"), nullable=False)
    id_stock = Column(Integer, ForeignKey("STOCK.id"), nullable=False)

    proveedor = relationship("Proveedor", back_populates="stock_items")
    stock = relationship("Stock", back_populates="proveedores")
