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
