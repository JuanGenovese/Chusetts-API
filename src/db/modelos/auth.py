from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base, TimestampMixin

class CuentaAuth(Base, TimestampMixin):
    __tablename__ = "CUENTAS"
    __table_args__ = {"schema": "auth"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    tipo_usuario = Column(String(25), nullable=False)  # 'ADM' | 'CLI'
    usuario_adm_id = Column(Integer, ForeignKey("USUARIOS_ADM.id", ondelete="CASCADE"), nullable=True)
    usuario_cli_id = Column(Integer, ForeignKey("USUARIOS_CLI.id", ondelete="CASCADE"), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    usuario_adm = relationship("UsuarioAdm", backref="cuenta_auth", uselist=False)
    usuario_cli = relationship("UsuarioCli", backref="cuenta_auth", uselist=False)
